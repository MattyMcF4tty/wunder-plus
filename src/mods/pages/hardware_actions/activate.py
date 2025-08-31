from playwright.sync_api import Page
from . import action_tap

def activate (page: Page):
  print("[Details] Activating hardware-actions modifications...")

  # action_tap.allow_tap(page)
