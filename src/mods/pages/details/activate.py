from playwright.sync_api import Page
from . import sort_tasks


def activate (page: Page):
  sort_tasks.newest_task_first(page)
