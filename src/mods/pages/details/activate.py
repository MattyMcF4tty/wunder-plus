from playwright.sync_api import Page
from . import sort_tasks


def activate (page: Page):
  print("[Details] Activating details page modifications...")

  sort_tasks.newest_first(page)
