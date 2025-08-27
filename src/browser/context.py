from playwright.sync_api import BrowserContext
from ..cache import cookies
from .storage import inject_map_settings

def setup_context(context: BrowserContext) -> None:
  # Load cached cookies from last session
  cached_cookies = cookies.read()
  if cached_cookies:
    print(f'Injecting {len(cached_cookies)} cached cookies into browser context')
    context.add_cookies(cached_cookies)

  # Inject map settings into every new page
  context.on("page", inject_map_settings)