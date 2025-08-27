import json
from ..config import CACHE_FILE

def create_cache_file():
  print("Creating new cache file")
  # Make sure the directory exists
  CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
  with CACHE_FILE.open("w", encoding="utf-8") as file:
    json.dump({'cookies': [], 'map_settings': {}}, file, indent=2, ensure_ascii=False)


def read_cache_file():

  if not CACHE_FILE.exists():
    create_cache_file()

  with CACHE_FILE.open("r", encoding="utf-8") as file:
    data = json.load(file)
  
  return data
  

def save_cache_file(data: dict) -> None:
  if not CACHE_FILE.exists():
    create_cache_file()

  with CACHE_FILE.open("w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)