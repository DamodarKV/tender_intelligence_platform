from fastapi import Request
from fastapi.responses import RedirectResponse


def authenticate(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)

    return None