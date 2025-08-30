import json
from playwright.sync_api import BrowserContext
from ..cache import map_settings
from typing import Any

def inject_map_settings_init(context: BrowserContext) -> None:
  cached_settings = map_settings.read()

  if cached_settings:
    print("Injecting mapSettings into localStorage")

    json_settings = json.dumps(cached_settings)
    context.add_init_script(
      f"""
      try {{
        console.log('Injecting mapSettings into localStorage');
        localStorage.setItem('mapSettings', JSON.stringify({json_settings}));
      }} catch (e) {{
        console.error('mapSettings injection failed', e);
      }}
      """
    )