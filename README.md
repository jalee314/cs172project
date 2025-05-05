# CS 172 Project

CS172 Reddit Crawler

# Running the Program 

For Mac/Linux Users, follow these commands to set up your virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Window Users, follow these commands to set up your virtual environment

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


For Window users, you can run the crawler by either double clicking the batch file or by inputting in powershell
```
.\crawler.bat <num_threads> <max_file_size_mb>
```
* num_threads (optional): Number of worker threads to use (default: 10)

* max_file_size_mb (optional): Max size of each JSON file in MB (default: 10)
