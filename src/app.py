from playwright.sync_api import sync_playwright
from .config import DEFAULT_PAGE
from .browser import setup_context
from .mods import initialize


def start():
  print('Starting Wunder+')

  # Own the Playwright lifecycle here
  with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(no_viewport=True, viewport=None, permissions=['geolocation'])

    setup_context(context)

    # Attach mods initializer
    context.on('page', initialize)

    # Open first page
    page = context.new_page()
    page.goto(DEFAULT_PAGE)


    # Keep the alive
    while True:
      pages = context.pages
      if not pages:
        break

      pages[0].wait_for_event("close", timeout=0)

  print('Exiting Wunder+')