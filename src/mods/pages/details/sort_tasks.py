from playwright.sync_api import Page, Locator

# Make newest tasks always appear first
def newest_first(page: Page) -> None:
  if '?' in page.url and '#tasks' not in page.url:
    return
  
  list_container = page.locator("#tasks").locator("div.grid-body")
  rows = list_container.locator(":scope > div.row[data-key]")

  pairs: list[tuple[int, Locator]] = []
  for i in range(rows.count()):
    row = rows.nth(i)
    key_str = row.get_attribute("data-key")
    if key_str is None:
      continue
    try:
      key = int(key_str)
    except ValueError:
      # We skip rows with non-numeric data-key
      continue
    pairs.append((key, row))

  for _, row in sorted(pairs, key=lambda x: x[0], reverse=True):
    row.evaluate("el => el.parentElement.appendChild(el)")
  