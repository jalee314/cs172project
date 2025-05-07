# CS 172 Project

# Reddit Crawler

## Running the Crawler 

For Mac/Linux Users, follow these commands to set up your virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows Users, follow these commands to set up your virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
For Mac/Linux users, you can run the crawler using the provided shell script:

```
./crawler.sh <num_threads> <max_file_size_mb>
```

* num_threads (optional): Number of worker threads to use (default: 10)

* max_file_size_mb (optional): Max size of each JSON file in MB (default: 10)


For Windows users, you can run the crawler by either double clicking the batch file or by typing in Powershell
```
.\crawler.bat <num_threads> <max_file_size_mb>
```
* num_threads (optional): Number of worker threads to use (default: 10)

* max_file_size_mb (optional): Max size of each JSON file in MB (default: 10)

## Crawler Architecture
![crawlerdiagram drawio(killswitch)](https://github.com/user-attachments/assets/5a5f46a5-6939-4378-a6fe-85a2887a15a8)

## System Limitations & Benchmark Results

### Thread Count Benchmarking

We tested the Reddit crawler using varying thread counts and two JSON file size caps (1MB and 10MB). Major gains were seen up to **20 threads**, with runtime dropping by over **85%** compared to the single-threaded baseline. Optimal performance occurred around **40 threads**, where we observed the fastest crawl time.

#### Max File Size: 1MB

| Thread Count | Time to Run (s) |
|--------------|-----------------|
| 1            | 758.66          |
| 5            | 206.20          |
| 10           | 133.63          |
| 15           | 110.48          |
| 20           | 99.85           |
| 30           | 110.88          |
| 40           | 93.71           |
| 50           | 99.91           |

#### Max File Size: 10MB

| Thread Count | Time to Run (s) |
|--------------|-----------------|
| 1            | 742.33          |
| 5            | 199.82          |
| 10           | 129.90          |
| 15           | 106.90          |
| 20           | 96.40           |
| 30           | 108.20          |
| 40           | 91.40           |
| 50           | 9780.00         |

**Note**: Increasing the file size cap from 1MB to 10MB resulted in a **2–5% improvement in runtime**, due to reduced file I/O overhead in the `SaverThread`.

### Conclusion

Using **20–40 threads** offers the best tradeoff between speed and stability. While additional threads beyond this range do not consistently improve performance, they also do not significantly degrade it under our test conditions.

---

## Rate Limit Stress Testing

Reddit's API rate limiting began to impact performance between **30–50 threads**, even though [PRAW](https://praw.readthedocs.io/) attempts to handle rate limits automatically. This aligns with the performance fluctuations observed beyond 20–30 threads, largely attributed to:

- Reddit API rate limits
- Network latency
- Shared system resources
