import logging
from .session import SessionManager
from .parser import parse_dropdown

log = logging.getLogger(__name__)


class TraversalEngine:

    def __init__(self):
            self.session = SessionManager()

                def run(self, select_name: str):
                        log.info("Loading initial page...")
                                soup = self.session.load()
                                        self._traverse_first_level(soup, select_name)

                                            def _traverse_first_level(self, soup, select_name: str):
                                                    options = parse_dropdown(soup, select_name)

                                                            if not options:
                                                                        log.warning("No options found in dropdown: %s", select_name)
                                                                                    return

                                                                                            log.info("Found %d options in '%s'.", len(options), select_name)

                                                                                                    for value, text in options:
                                                                                                                log.info("Processing: %s", text)

                                                                                                                            updated_soup = self.session.postback(
                                                                                                                                            event_target=select_name,
                                                                                                                                                            selections={select_name: value},
                                                                                                                                                                        )

                                                                                                                                                                                    # Placeholder for next level traversal.
                                                                                                                                                                                                _ = updated_soup