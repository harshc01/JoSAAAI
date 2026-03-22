import time
import logging
import requests
from bs4 import BeautifulSoup
from .config import BASE_URL, HEADERS, RETRY_COUNT, TIMEOUT

log = logging.getLogger(__name__)

DELAY = 1.5
RETRY_BACKOFF = 3
HIDDEN_FIELDS = ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]


class SessionManager:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.hidden = {}

    def load(self) -> BeautifulSoup:
        resp = self._get()
        soup = BeautifulSoup(resp.text, "lxml")
        self._update_hidden(soup)
        return soup

    def postback(self, event_target: str, selections: dict) -> BeautifulSoup:
        payload = {
            "__EVENTTARGET": event_target,
            "__EVENTARGUMENT": "",
            **self.hidden,
            **selections,
        }
        return self._post(payload)

    def _update_hidden(self, soup: BeautifulSoup):
        for field in HIDDEN_FIELDS:
            tag = soup.find("input", {"name": field})
            self.hidden[field] = tag["value"] if tag and tag.get("value") else ""

    def _get(self) -> requests.Response:
        for attempt in range(1, RETRY_COUNT + 1):
            try:
                resp = self.session.get(BASE_URL, timeout=TIMEOUT)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                self._handle_error(e, attempt)
        raise RuntimeError("GET failed after retries")

    def _post(self, payload: dict) -> BeautifulSoup:
        time.sleep(DELAY)
        for attempt in range(1, RETRY_COUNT + 1):
            try:
                resp = self.session.post(BASE_URL, data=payload, timeout=TIMEOUT)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "lxml")
                self._update_hidden(soup)
                return soup
            except requests.RequestException as e:
                self._handle_error(e, attempt)
        raise RuntimeError("POST failed after retries")

    def _handle_error(self, exc: Exception, attempt: int):
        if attempt == RETRY_COUNT:
            raise exc
        wait = RETRY_BACKOFF * attempt
        log.warning("Retry %d/%d after error: %s", attempt, RETRY_COUNT, exc)
        time.sleep(wait)
