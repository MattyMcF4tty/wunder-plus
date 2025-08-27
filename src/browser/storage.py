from playwright.sync_api import Page
from ..cache import map_settings
import json


def inject_map_settings(page: Page):
  cached_map_settings = map_settings.read()

  page.add_init_script(f"""
    () => {{
      localStorage.setItem("map_settings", '{cached_map_settings}');
    }}
  """)