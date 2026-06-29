from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database.excel_db import get_all_tenders, get_tender_by_id

# CRITICAL FIX: Define the APIRouter instance first!
router = APIRouter(prefix="/tenders")
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def list_tenders(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(
            "/login",
            status_code=303
        )
    tenders = get_all_tenders()
    return templates.TemplateResponse(request, "tenders.html", {"tenders": tenders})


@router.get("/{tender_id}", response_class=HTMLResponse)
async def view_tender_detail(request: Request, tender_id: str):
    if not request.session.get("user"):
        return RedirectResponse(
            "/login",
            status_code=303
        )
    tender = get_tender_by_id(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Requested Tender data could not be located.")

    return templates.TemplateResponse(request, "tender_detail.html", {"tender": tender})