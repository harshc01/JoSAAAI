import csv
import os


def save_to_csv(records: list[dict], file_path: str) -> int:
    if not records:
            return 0

                records = _deduplicate(records)
                    file_exists = os.path.isfile(file_path)
                        existing = _load_existing(file_path) if file_exists else set()

                            headers = list(records[0].keys())
                                new_records = [r for r in records if _row_key(r) not in existing]

                                    if not new_records:
                                            return 0

                                                os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

                                                    with open(file_path, "a", newline="", encoding="utf-8") as f:
                                                            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
                                                                    if not file_exists or os.path.getsize(file_path) == 0:
                                                                                writer.writeheader()
                                                                                        writer.writerows(new_records)

                                                                                            return len(new_records)


                                                                                            def _deduplicate(records: list[dict]) -> list[dict]:
                                                                                                seen = set()
                                                                                                    unique = []
                                                                                                        for record in records:
                                                                                                                key = _row_key(record)
                                                                                                                        if key not in seen:
                                                                                                                                    seen.add(key)
                                                                                                                                                unique.append(record)
                                                                                                                                                    return unique


                                                                                                                                                    def _load_existing(file_path: str) -> set:
                                                                                                                                                        existing = set()
                                                                                                                                                            with open(file_path, "r", encoding="utf-8") as f:
                                                                                                                                                                    reader = csv.DictReader(f)
                                                                                                                                                                            for row in reader:
                                                                                                                                                                                        existing.add(_row_key(row))
                                                                                                                                                                                            return existing


                                                                                                                                                                                            def _row_key(record: dict) -> tuple:
                                                                                                                                                                                                return tuple(sorted((k, str(v)) for k, v in record.items()))