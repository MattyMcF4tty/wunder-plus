from playwright.sync_api import Page
from . import details

def router(page: Page):
  if '/details' in page.url:
    details.activate(page)