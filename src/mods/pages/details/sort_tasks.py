from playwright.sync_api import Page

# Make newest tasks always appear first
def newest_first(page: Page):
  if 'car/' in page.url and '?' not in page.url:
    car_id = page.url.rsplit("/", 1)[-1]
    new_url = f"{page.url}?car%{car_id}=&dp-4-sort=-createTime"
    page.goto(new_url)