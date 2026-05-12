import re
from typing import Any
import urllib.parse
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def _parse_rating(label: str | None) -> float | None:
    if not label:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", label)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _first_text(page, selectors: list[str]) -> str | None:
    for selector in selectors:
        locator = page.locator(selector)
        if locator.count() > 0:
            value = (locator.first.inner_text()).strip()
            if value:
                return value
    return None


def scrape_google_maps(city: str, category: str, max_results: int = 20) -> list[dict[str, Any]]:
    query = f"{category} in {city}"
    results: list[dict[str, Any]] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(locale="en-US")
        page = context.new_page()

        encoded_query = urllib.parse.quote(query)
        page.goto(f"https://www.google.com/maps/search/{encoded_query}", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        feed = page.locator('div[role="feed"]')
        feed.wait_for(timeout=15000)

        for _ in range(6):
            feed.evaluate("el => el.scrollBy(0, el.scrollHeight)")
            page.wait_for_timeout(600)

        cards = page.locator('a[href*="/maps/place"]')
        card_count = cards.count()
        limit = min(card_count, max_results)

        for idx in range(limit):
            card = cards.nth(idx)
            try:
                card.click(timeout=5000)
                page.wait_for_timeout(900)
            except PlaywrightTimeoutError:
                continue

            name = _first_text(page, ["h1.DUwDvf", "h1.fontHeadlineLarge"])
            if not name:
                continue

            address = _first_text(
                page,
                [
                    'button[data-item-id="address"] .Io6YTe',
                    'div[aria-label="Address"] .Io6YTe',
                ],
            )
            phone = _first_text(
                page,
                [
                    'button[data-item-id^="phone"] .Io6YTe',
                    'div[aria-label^="Phone"] .Io6YTe',
                ],
            )
            detected_category = _first_text(
                page,
                [
                    'button[jsaction*="pane.rating.category"]',
                    "button.DkEaL",
                ],
            )

            rating = None
            rating_label_locator = page.locator('span[role="img"][aria-label*="star"]')
            if rating_label_locator.count() > 0:
                rating_label = rating_label_locator.first.get_attribute("aria-label")
                rating = _parse_rating(rating_label)

            results.append(
                {
                    "name": name,
                    "address": address or "N/A",
                    "phone": phone or "N/A",
                    "rating": rating,
                    "category": (detected_category or category).strip(),
                    "city": city.strip(),
                }
            )

        context.close()
        browser.close()

    return results
