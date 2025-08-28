from playwright.sync_api import Page, BrowserContext
from ...cache import cookie_store

_AUTH_FLOW_FLAG = '_wunder_auth_flow'


def flow_handler (page: Page):
    # Handle the wunder auth flow and save auth cookies
  if 'login' in page.url and not hasattr(page, _AUTH_FLOW_FLAG):
    print("Detected auth flow, waiting for user to complete...")
    cookie_store.clear()
    setattr(page, _AUTH_FLOW_FLAG, True)
  elif hasattr(page, _AUTH_FLOW_FLAG):
    print("Auth flow completed, saving cookies...")
    context = page.context
    auth_cookies = get_auth_cookies(context)
    cookie_store.write(auth_cookies)
    delattr(page, _AUTH_FLOW_FLAG)


def get_auth_cookies(context: BrowserContext) -> list[cookie_store.Cookie]:
    print("Obtaining cookies...")
    cookies = context.cookies()

    # the cookie names you want to extract
    static_wanted = {"PHPSESSID", "_csrf-backend", "_ga", "_identity", "_mfa-device-token"}
    dynamic_prefixes = {"_ga_", "_hjSessionUser_", "_hjSession_",}

    # Select only the cookies we care about
    selected = [
        cookie_store.filter_cookie(c)
        for c in cookies
        if (name := c.get("name"))
        and (name in static_wanted or any(name.startswith(prefix) for prefix in dynamic_prefixes))
    ]



    if len(selected) == 0:
        print("Found no matching cookies in browser")
    else:
        print("Found", len(selected), "matching cookies")

    return selected