import csv
import logging
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
log = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CSV_PATH = "data/output.csv"
TABLE = "seat_allotments"
BATCH_SIZE = 500


def load_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def upload(records: list[dict]):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    total = len(records)
    uploaded = 0

    for i in range(0, total, BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        client.table(TABLE).insert(batch).execute()
        uploaded += len(batch)
        log.info("Uploaded %d / %d", uploaded, total)

    log.info("Done. Total uploaded: %d", uploaded)


if __name__ == "__main__":
    records = load_csv(CSV_PATH)
    log.info("Loaded %d records from CSV.", len(records))
    upload(records)