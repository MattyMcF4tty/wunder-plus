from playwright.sync_api import sync_playwright
from .config import DEFAULT_PAGE
from .browser import setup_context
from .mods import initialize


def start():
  print('Starting Wunder+')

  # Own the Playwright lifecycle here
  with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(viewport=None, permissions=['geolocation'])

    # All context mutations must happen while Playwright is alive
    setup_context(context)

    # Open first page
    page = context.new_page()
    page.goto(DEFAULT_PAGE)

    # Attach mods initializer for any subsequently opened pages.
    # IMPORTANT: pass the callable, don't call it immediately.
    context.on('page', initialize)

    # Keep the process alive until all pages are closed
    while True:
      pages = context.pages
      if not pages:
        break

      # Wait for the first page to close before checking again
      pages[0].wait_for_event("close", timeout=0)

  print('Exiting Wunder+')