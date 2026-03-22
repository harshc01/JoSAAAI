import argparse
import logging
from .traversal import TraversalEngine
from .storage import save_to_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger(__name__)


def main(output_path: str):
    engine = TraversalEngine()

    log.info("Starting traversal...")
    records = engine.run()
    log.info("Total records scraped: %d", len(records))

    saved = save_to_csv(records, output_path)
    log.info("Records saved to '%s': %d", output_path, saved)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JoSAA scraper")
    parser.add_argument(
        "--output",
        default="data/output.csv",
        help="Output CSV file path (default: data/output.csv)",
    )
    args = parser.parse_args()
    main(args.output)
