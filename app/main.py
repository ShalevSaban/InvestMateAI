from fastapi import FastAPI
from app.routes import agents, properties, auth, public_properties, gpt, dashboard_insights
from app.database import create_tables


app = FastAPI(title="InvestMateAI")

app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard_insights.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(public_properties.router)
app.include_router(gpt.router)


@app.on_event("startup")
def on_startup():
    create_tables()
