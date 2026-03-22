from bs4 import BeautifulSoup

NULL_OPTIONS = {"", "0", "select", "--select--", "select..."}
RESULT_TABLE_ID = "ctl00_ContentPlaceHolder1_GridView1"

COLUMN_MAP = {
    "Institute": "institute",
    "Academic Program Name": "program",
    "Quota": "quota",
    "Seat Type": "category",
    "Gender": "gender",
    "Opening Rank": "opening_rank",
    "Closing Rank": "closing_rank",
}


def parse_dropdown(soup: BeautifulSoup, select_name: str) -> list[tuple[str, str]]:
    sel = soup.find("select", {"name": select_name})
    if not sel:
        sel = soup.find("select", {"id": select_name.replace("$", "_")})
    if not sel:
        return []

    return [
        (opt.get("value", "").strip(), opt.get_text(strip=True))
        for opt in sel.find_all("option")
        if opt.get("value", "").strip().lower() not in NULL_OPTIONS
    ]


def parse_table(soup: BeautifulSoup) -> list[dict]:
    table = soup.find("table", {"id": RESULT_TABLE_ID}) or soup.find("table")
    if not table:
        return []
        
    rows = table.find_all("tr")
    if len(rows) < 2:
        return []

    headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]
        
    records = []
    for row in rows[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cells:
            continue
                
        record = {}
        for header, value in zip(headers, cells):
            key = COLUMN_MAP.get(header.strip())
            if key is None:
                continue
            record[key] = value if value not in ("", "---", "N/A") else None
                    
        if record:
            records.append(record)
                    
    return records
