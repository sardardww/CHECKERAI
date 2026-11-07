from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from karakalpak_ai_master import (
    sanitize_and_proofread_post,
    evaluate_news_relevance,
    repair_rogue_capital_i,
    cyrillic_to_karakalpak_latin
)

app = FastAPI(title="CHECKERAI API", version="1.0.0")

class CheckRequest(BaseModel):
    text: str
    source_url: Optional[str] = ""

class CheckResponse(BaseModel):
    is_relevant: bool
    relevance_reason: str
    cleaned_html: str
    original_text: str

@app.get("/")
def index():
    return {"status": "ok", "service": "CHECKERAI Karakalpak 0-Error Linguistic API"}

@app.post("/check", response_model=CheckResponse)
def check_text(req: CheckRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    is_rel, rel_reason = evaluate_news_relevance(req.text)
    cleaned = sanitize_and_proofread_post(req.text, req.source_url or "")
    return CheckResponse(
        is_relevant=is_rel,
        relevance_reason=rel_reason,
        cleaned_html=cleaned,
        original_text=req.text
    )

@app.post("/transliterate")
def transliterate_cyrillic(req: CheckRequest):
    latin = cyrillic_to_karakalpak_latin(req.text)
    return {"cyrillic": req.text, "latin": latin}
