from fastapi import FastAPI
from routers import dashboard, tenders, auth
from starlette.middleware.sessions import SessionMiddleware

#app = FastAPI()


app = FastAPI(title="Tender Intelligence Platform")
app.add_middleware(
    SessionMiddleware,
    secret_key="TenderPlatformSecretKey"
)


# Mount Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(tenders.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)