@router.get("/", response_class=HTMLResponse)
async def list_tenders(request: Request):
    tenders = get_all_tenders()
    # Pass request first 👇
    return templates.TemplateResponse(request, "tenders.html", {"tenders": tenders})


@router.get("/{tender_id}", response_class=HTMLResponse)
async def view_tender_detail(request: Request, tender_id: str):
    tender = get_tender_by_id(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Requested Tender data could not be located.")

    # Pass request first 👇
    return templates.TemplateResponse(request, "tender_detail.html", {"tender": tender})