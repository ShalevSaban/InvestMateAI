from fastapi import FastAPI
from app.routes import agents, properties, auth, public_properties, gpt, dashboard_insights
from app.database import create_tables
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from app.telegram.webhook import router as telegram_router
from fastapi.responses import FileResponse
from app.routes import agents, properties, auth, public_properties, gpt, dashboard_insights, cleanup

app = FastAPI(title="InvestMateAI")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard_insights.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(public_properties.router)
app.include_router(gpt.router)
app.include_router(telegram_router)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.include_router(cleanup.router, prefix="/cleanup", tags=["Cleanup"])


@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")