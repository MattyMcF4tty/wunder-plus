from playwright.sync_api import Page, Frame
from ..config import DOMAIN_NAME, LISTENER_TAG
from .pages import router
from .flows import auth

def initialize(page: Page) -> None:

  # If we're not on the correct domain, clear listener tag
  if DOMAIN_NAME not in page.url:
    if hasattr(page, LISTENER_TAG):
      delattr(page, LISTENER_TAG)
    return

  # Guard: only attach the listener once per page
  if getattr(page, LISTENER_TAG, False):
    return

  setattr(page, LISTENER_TAG, True)

  def on_frame_navigated(frame: Frame) -> None:
    # We avoid ads and videos by only detecting the main frame
    if frame != page.main_frame:
      return
    if DOMAIN_NAME in page.url:
      on_navigation(page)

  page.on("framenavigated", on_frame_navigated)

  # Run once on initialization
  on_navigation(page)


# When a page is navigated to

def on_navigation(page: Page):
  print(f"[Mod] Navigated to {page.url}")
  # Flows
  auth.flow_handler(page)

  # Pages
  router(page)
  
