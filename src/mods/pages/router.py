from playwright.sync_api import Page
from . import details, hardware_actions

def router(page: Page):
  
  if '/car' in page.url:
    details.activate(page)

  if '/hardware-actions' in page.url:
    hardware_actions.activate(page)