import logging
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page

from scraper.parser import parse_table
from scraper.storage import save_to_csv

log = logging.getLogger(__name__)

URL = "https://josaa.admissions.nic.in/Applicant/seatallotmentresult/currentorcr.aspx"
OUTPUT_PATH = "data/output.csv"


def _extract(page: Page) -> list[dict]:
    soup = BeautifulSoup(page.content(), "lxml")
    return parse_table(soup)


class PlaywrightTraversal:

    def run(self):
        results: list[dict] = []

        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",
                ],
            )
            page = browser.new_page()

            log.info("Loading JoSAA page...")
            page.goto(URL, timeout=60_000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)

            round_count = page.locator("select").nth(0).locator("option").count()
            log.info("Rounds found: %d", round_count - 1)

            try:
                for i in range(1, round_count):
                    log.info("Processing round %d...", i)
                    try:
                        page.locator("select").nth(0).select_option(index=i, force=True)
                        page.wait_for_timeout(2000)
                        page.locator("select").nth(1).select_option(index=1, force=True)
                        page.wait_for_timeout(2000)
                        page.locator("select").nth(2).select_option(index=1, force=True)
                        page.wait_for_timeout(2000)
                        page.locator("select").nth(3).select_option(index=1, force=True)
                        page.wait_for_timeout(2000)
                        page.locator("select").nth(4).select_option(index=1, force=True)
                        page.wait_for_timeout(2000)

                        page.get_by_role("button", name="Submit").click(force=True)
                        page.wait_for_load_state("networkidle")
                        page.wait_for_timeout(3000)

                        records = _extract(page)
                        log.info("Round %d: +%d rows.", i, len(records))
                        results.extend(records)

                    except Exception as exc:
                        log.error("Round %d failed: %s — reloading page.", i, exc)
                        page.goto(URL, timeout=60_000)
                        page.wait_for_load_state("networkidle")
                        page.wait_for_timeout(3000)
                        continue

            finally:
                if results:
                    saved = save_to_csv(results, OUTPUT_PATH)
                    log.info("Saved %d records to %s.", saved, OUTPUT_PATH)
                browser.close()

        log.info("Done.")