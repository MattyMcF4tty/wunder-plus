from typing import TypedDict
from .store import read_cache_file, save_cache_file


class Cookie(TypedDict):
  name: str
  value: str
  domain: str
  path: str
  expires: float


def write(updatedCookies: list[Cookie]):
  print('Updating cookies in cache...')
  cache = read_cache_file()
  cache["cookies"] = updatedCookies
  save_cache_file(cache)


def read() -> list[dict]:
  print("Reading cookies cache...")
  cache = read_cache_file()
  cachedCookies = cache['cookies'] or []

  print("Found", len(cachedCookies), "cookies in cache")
  return cachedCookies

def reset():
  print("Resetting cookies in cache...")

  cache = read_cache_file()

  cache['cookies'] = []

  save_cache_file(cache)

