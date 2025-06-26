from fastapi import FastAPI
from app.routes import agents, properties, auth
from app.database import create_tables

app = FastAPI(title="InvestMateAI")

app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.on_event("startup")
def on_startup():
    create_tables()
