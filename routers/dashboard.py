from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.excel_db import get_all_tenders

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_dashboard(
        request: Request,
        title: str = "",
        min_value: str = "",
        max_value: str = "",
        location: str = "",
        status: str = ""
):
    all_tenders = get_all_tenders()
    filtered_tenders = []

    for tender in all_tenders:
        # 1. Title Filter
        if title and title.lower() not in tender.get("title", "").lower():
            continue

        # 2. Status Filter
        if status and status.lower() not in tender.get("status", "").lower():
            continue

        # 3. Work Location Filter
        loc_match = False
        for k, v in tender.items():
            if "location" in k and location.lower() in str(v).lower():
                loc_match = True
                break
        if location and not loc_match:
            continue

        # 4. Tender Value RANGE Filter
        if tender.get("value") is not None:
            try:
                current_val = float(tender.get("value", 0))

                # Check Minimum Boundary
                if min_value and current_val < float(min_value):
                    continue

                # Check Maximum Boundary
                if max_value and current_val > float(max_value):
                    continue
            except ValueError:
                pass  # Skip parsing errors on corrupted row values safely

        filtered_tenders.append(tender)

    total_tenders = len(all_tenders)
    total_value = sum(t.get("value", 0) for t in all_tenders)
    open_tenders = len([t for t in all_tenders if t.get("status") == "Open"])

    # Change from: templates.TemplateResponse("dashboard.html", {...})
    # To this:
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "total_tenders": total_tenders,
            "total_value": total_value,
            "open_tenders": open_tenders,
            "tenders": filtered_tenders,
            "filters": {
                "title": title,
                "min_value": min_value,
                "max_value": max_value,
                "location": location,
                "status": status
            }
        }
    )