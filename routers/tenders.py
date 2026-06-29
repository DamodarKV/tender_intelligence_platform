from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.excel_db import get_all_tenders, get_tender_by_id
from utils.auth import authenticate

# CRITICAL FIX: Define the APIRouter instance first!
router = APIRouter(prefix="/tenders")
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def list_tenders(request: Request):
    auth = authenticate(request)

    if auth:
        return auth

    tenders = get_all_tenders()
    return templates.TemplateResponse(request, "tenders.html", {"tenders": tenders})


@router.get("/{tender_id}", response_class=HTMLResponse)
async def view_tender_detail(request: Request, tender_id: str):
    auth = authenticate(request)

    if auth:
        return auth

    tender = get_tender_by_id(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Requested Tender data could not be located.")

    return templates.TemplateResponse(request, "tender_detail.html", {"tender": tender})