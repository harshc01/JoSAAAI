import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

TOOL_DEFINITION = {
    "name": "search_allotments",
    "description": "Search JoSAA seat allotment data for opening and closing ranks",
    "parameters": {
        "type": "object",
        "properties": {
            "institute": {
                "type": "string",
                "description": "Institute name e.g. 'Indian Institute of Technology Bombay'"
            },
            "program": {
                "type": "string",
                "description": "Program name e.g. 'Computer Science and Engineering'"
            },
            "category": {
                "type": "string",
                "description": "Category e.g. OPEN, EWS, OBC-NCL, SC, ST"
            },
            "round": {
                "type": "string",
                "description": "Round number e.g. 'Round 1'"
            },
        },
    }
}


def search_allotments(
    institute: str = None,
    program: str = None,
    category: str = None,
    round: str = None,
) -> list[dict]:
    query = supabase.table("seat_allotments").select("*")

    if institute:
        query = query.ilike("institute", f"%{institute}%")
    if program:
        query = query.ilike("program", f"%{program}%")
    if category:
        query = query.ilike("category", f"%{category}%")
    if round:
        round_num = ''.join(filter(str.isdigit, round))
        if round_num:
            query = query.eq("round", int(round_num))

    query = query.limit(100)
    result = query.execute()
    return result.data