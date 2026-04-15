from fastapi import APIRouter, Query
from api.tools import supabase

router = APIRouter()


@router.get("/predict")
async def predict(
    rank: int,
    category: str = "OPEN",
    gender: str = "Gender-Neutral",
    quota: str = "AI",
    round: int = 6,
):
    result = (
        supabase.table("seat_allotments")
        .select("*")
        .eq("category", category)
        .eq("gender", gender)
        .eq("quota", quota)
        .eq("round", round)
        .lte("closing_rank", rank)
        .order("closing_rank", desc=True)
        .limit(50)
        .execute()
    )
    rows = result.data
    for r in rows:
        diff = rank - int(r["closing_rank"])
        if diff <= 2000:
            r["chance"] = "safe"
        elif diff <= 8000:
            r["chance"] = "target"
        else:
            r["chance"] = "dream"
    return {"data": rows, "count": len(rows)}


@router.get("/explore")
async def explore(
    institute: str = None,
    program: str = None,
    category: str = None,
    round: int = None,
    min_rank: int = None,
    max_rank: int = None,
    limit: int = 50,
    offset: int = 0,
):
    query = supabase.table("seat_allotments").select("*")
    if institute:
        query = query.ilike("institute", f"%{institute}%")
    if program:
        query = query.ilike("program", f"%{program}%")
    if category:
        query = query.eq("category", category)
    if round:
        query = query.eq("round", round)
    if min_rank:
        query = query.gte("closing_rank", min_rank)
    if max_rank:
        query = query.lte("closing_rank", max_rank)
    result = query.order("closing_rank").range(offset, offset + limit - 1).execute()
    return {"data": result.data, "count": len(result.data)}


@router.get("/trends")
async def trends(institute: str = None, program: str = None, category: str = "OPEN"):
    query = (
        supabase.table("seat_allotments")
        .select("round,opening_rank,closing_rank,institute,program")
        .eq("category", category)
        .order("round")
    )
    if institute:
        query = query.ilike("institute", f"%{institute}%")
    if program:
        query = query.ilike("program", f"%{program}%")
    result = query.limit(200).execute()
    return {"data": result.data}


@router.get("/compare")
async def compare(institutes: str = Query(...), program: str = None, category: str = "OPEN"):
    names = [i.strip() for i in institutes.split(",")]
    all_data = []
    for name in names:
        query = (
            supabase.table("seat_allotments")
            .select("*")
            .ilike("institute", f"%{name}%")
            .eq("category", category)
        )
        if program:
            query = query.ilike("program", f"%{program}%")
        result = query.order("round").limit(50).execute()
        all_data.extend(result.data)
    return {"data": all_data}


@router.get("/institutes")
async def institutes():
    result = supabase.table("seat_allotments").select("institute").execute()
    names = sorted(set(r["institute"] for r in result.data))
    return {"data": names}


@router.get("/programs")
async def programs():
    result = supabase.table("seat_allotments").select("program").execute()
    names = sorted(set(r["program"] for r in result.data))
    return {"data": names}
