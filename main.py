from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from routers import dashboard, tenders, auth

app = FastAPI(title="Tender Intelligence Platform")

app.add_middleware(
    SessionMiddleware,
    secret_key="TenderPlatformSecret123"
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(tenders.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)