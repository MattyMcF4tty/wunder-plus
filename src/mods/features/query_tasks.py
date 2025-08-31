import requests
from ...cache import cookie_store
import time
from config import DOMAIN_NAME

def query_tasks() -> None:
  query_term = '500 degrees'


  cached_cookies = cookie_store.read()
  cookies = {cookie["name"]: cookie["value"] for cookie in cached_cookies}
  
  page = 0
  more_pages = True
  while more_pages:
    time.sleep(5)
    page += 1
    print(f"Fetching tasks from page {page}...")
    url = f'https://{DOMAIN_NAME}/api/v2/tasks/search?sort=-createTime&fields=taskId,carId,title,description,taskStateId,assignedUserJSON,notifyAssignedUsers,priority,dueDate,customerId,uploadedFiles,uploadedFileId,s3URL&per-page=100&page={page}'

    response = requests.post(url, cookies=cookies)
    if response.status_code != 200:
      print(f"Error fetching tasks: {response.status_code}")
      continue

    data = response.json()
    tasks = data.get("data", [])
    
    print(f"Fetched {len(tasks)} tasks from page {page}")
    if len(tasks) != 100:
      more_pages = False

    for task in tasks:
      title = task.get("title", "") or ""
      description = task.get("description", "") or ""
      if query_term.lower() in title.lower() or query_term.lower() in description.lower():
        print(f"Match found! Task ID: {task['taskId']}, Car ID: {task['carId']}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print("------")
        more_pages = False
        break
    


  
  