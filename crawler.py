import praw
import threading 
import queue 
import time
import requests
import json
import os
from bs4 import BeautifulSoup

class SaverThread(threading.Thread):
    
    def __init__(self, json_queue, directory=".", filename_prefix="data_", max_size_mb=1):
        super().__init__()
        self.json_queue = json_queue
        self.directory = directory
        self.filename_prefix = filename_prefix
        self.max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes

        self.file_counter = 1
        self.curr_file = None
        self.curr_file_size = 0

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_next_filename(self):
        return os.path.join(self.directory, f"{self.filename_prefix}{self.file_counter}.json")

    def start_new_file(self):
        try:
            self.curr_file = open(self.get_next_filename(), "w", encoding="utf-8")
            self.curr_file_size = 0
            return True
        except OSError as e:
            print(f"Error opening file: {e}")
            return False

    def run(self):
        global kill_switch

        try:
            if not self.start_new_file():
                print("Failed to begin saving data")
                return

            total_written = 0

            while True:
                try:
                    json_obj = self.json_queue.get(timeout=1)
                    json_data = json.dumps(json_obj, ensure_ascii=False)
                    self.curr_file.write(json_data + "\n")
                    self.curr_file_size += len(json_data.encode("utf-8")) + 1

                    if self.curr_file_size >= self.max_size_bytes:
                        self.curr_file.close()
                        self.file_counter += 1
                        if not self.start_new_file():
                            print(f"[Saver Thread] Failed to save data to new file #{self.file_counter}")
                            return

                    self.json_queue.task_done()

                except queue.Empty:
                    if kill_switch and self.json_queue.empty():
                        print("[Saver Thread] Queue is empty and kill_switch is set. Exiting.")
                        break
                    time.sleep(0.5)


        finally:
            if self.curr_file:
                self.curr_file.close()


def getHTMLTitle(url): 
    try:
        page = requests.get(url, timeout=3) #if no response after 3 seconds just abort 
        soup = BeautifulSoup(page.text, "html.parser") #opted to use page.text over page.content, text returns string while content returns byte just makes more sense
        return soup.title.string.strip() if soup.title else None #returns content of <title> tag if it exists 
    except:
        return None


#we cannot launch a worker for each post in the frontier, we need to limit the number of workers and distribute the work
def worker():

    while True:                     

        if kill_switch and post_frontier.empty():       
            break
      
        try:
            post = post_frontier.get(timeout=3)     #don't let the thread hang, move on if taking too long
        except queue.Empty:
            if kill_switch and post_frontier.empty():
                break
            continue

        post_dict_lock.acquire()        #lock the hashmap to prevent race conditions since multiple threads will be writing to it
        if post in post_dict:       
            post_dict_lock.release()
            post_frontier.task_done()       #let queue know thread is finished so that it doesn't hang 
            continue                    
        else:
            #if we have not, add it to the dict
            post_dict[post] = True
            post_dict_lock.release()

        try:
            #get the submission object from the url
            submission = reddit.submission(url=post)  
            submission.comments.replace_more(limit=0) 
            comments = [c.body for c in submission.comments.list()]     #Store comments from the submission as a list #https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
        
            post_json = {
                "id": submission.id,
                "author": str(submission.author),
                "created_utc": submission.created_utc,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "url": submission.url,
                "permalink": submission.permalink,
                "comments": comments
            }

             #from instructions: If a post contains a URL to an html page, get title of that page, and add title as an additional field of the post, that is, include it in the JSON of the post, so it becomes searchable in Part B.
            if submission.selftext.startswith("http") and not submission.url.startswith("https://www.reddit.com"):  
                html_title = getHTMLTitle(submission.url)
                if html_title:
                    post_json["linked_page_title"] = html_title 

            json_frontier.put(post_json)

            print(f"[Worker Thread] Processed Post: {submission.title}")

        except Exception as e:
            print(f"[Worker Thread] Error encountered processing post: {post}\n{e}")

        finally:
            post_frontier.task_done()



reddit = praw.Reddit(
    client_id="Epb2_BoxRkCg8Lg2ctrbyg",
    client_secret="PcpZsf-R6DqoxFcj9RLFRRAmwW0WFw",
    user_agent="windows:myredditapp:v1.0 by u/Square_Procedure5859",
)

#locks to safely manage access to shared resources, technically not needed "A global interpreter lock (GIL) is used internally to ensure that only one thread runs in the Python VM at a time" = no data races? 
post_dict_lock = threading.Lock()


#top level defined objects are global in python threads
post_frontier = queue.Queue() #posts we need to crawl, changed by the worker threads, accessed by the worker threads
json_frontier = queue.Queue() #json for save thread to save to disk, changed by the worker threads, accessed by the saver thread
post_dict = {} #to detect duplicate post links in main thread before creating a worker
kill_switch = False #to be changed by the saver thread to kill the main thread, alert workers when we hit the save limit


saver_thread = SaverThread(json_frontier, directory="output_files") #only one thread to save to disk, avoids conflicts for data access 
saver_thread.start()

#seeds for the worker threads, these are the subreddits we want to crawl
subreddits_list = ['askreddit']

#populate the post frontier with the seeds
for subreddit in subreddits_list:
    for submission in reddit.subreddit(subreddit).hot(limit=100):
        post_frontier.put(submission.url)

# Launch N worker threads that will pull from the post frontier and push to the json frontier
NUM_WORKERS = 10

worker_threads = []
for _ in range(NUM_WORKERS):
    t = threading.Thread(target=worker)
    t.start()
    worker_threads.append(t)

post_frontier.join()
json_frontier.join()

kill_switch = True

for t in worker_threads:
    t.join()

#kill the main thread when we hit the save limit in saver thread 

saver_thread.join()