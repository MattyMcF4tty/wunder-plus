from typing import TypedDict, NotRequired, Literal, Any, Mapping, cast
from .store import read_cache_file, save_cache_file


class Cookie(TypedDict):
  name: NotRequired[str]
  value: NotRequired[str]
  url: NotRequired[str | None]
  domain: NotRequired[str | None]
  path: NotRequired[str | None]
  expires: NotRequired[float | None]
  httpOnly: NotRequired[bool | None]
  secure: NotRequired[bool | None]
  sameSite: NotRequired[Literal['Lax', 'None', 'Strict'] | None]
  partitionKey: NotRequired[str | None]


ALLOWED_KEYS = set(Cookie.__annotations__.keys())

def filter_cookie(cookie: Mapping[str, Any]) -> Cookie:
  filtered: dict[str, Any] = {key: value for key, value in cookie.items() if key in ALLOWED_KEYS}
  return cast(Cookie, filtered)

def write(updatedCookies: list[Cookie]):
  print('Updating cookies in cache...')
  cache = read_cache_file()
  cache["cookies"] = updatedCookies
  save_cache_file(cache)


def read() -> list[Cookie]:
  print("Reading cookies cache...")
  cache = read_cache_file()
  cachedCookies = cache['cookies'] or []

  print("Found", len(cachedCookies), "cookies in cache")
  return cachedCookies

def clear():
  print("Clearing cookies in cache...")

  cache = read_cache_file()

  cache['cookies'] = []

  save_cache_file(cache)

