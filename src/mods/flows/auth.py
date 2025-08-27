from playwright.sync_api import Page, BrowserContext
from ...cache import cookies

_AUTH_FLOW_FLAG = '_wunder_auth_flow'


def flow_handler (page: Page):
    # Handle the wunder auth flow and save auth cookies
  if 'Enter your Verification Code' in page.title():
    print("Detected auth flow, waiting for user to complete...")
    setattr(page, _AUTH_FLOW_FLAG, True)
  elif hasattr(page, _AUTH_FLOW_FLAG):
    print("Auth flow completed, saving cookies...")
    context = page.context
    cookies = get_auth_cookies(context)
    cookies.write(cookies)
    delattr(page, _AUTH_FLOW_FLAG)
  else: 
    context = page.context
    cookies = get_auth_cookies(context)
    cookies.write(cookies)


def get_auth_cookies(context: BrowserContext) -> list[cookies.Cookie]:
    print("Obtaining cookies...")
    cookies = context.cookies()

    # the cookie names you want to extract
    static_wanted = {"PHPSESSID", "_csrf-backend", "_ga", "_identity", "_mfa-device-token"}
    dynamic_prefixes = {"_ga_", "_hjSessionUser_", "_hjSession_",}

    # Select only the cookies we care about
    selected = [
        c for c in cookies
        if c["name"] in static_wanted or any(c["name"].startswith(prefix) for prefix in dynamic_prefixes)
    ]

    filtered = [
        {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ""),
            "path": c.get("path", "/"),
            "expires": c.get("expires")
        }
        for c in selected
    ]

    if len(filtered) == 0:
        print("Found no matching cookies in browser")
    else:
        print("Found", len(filtered), "matching cookies")

    return filtered