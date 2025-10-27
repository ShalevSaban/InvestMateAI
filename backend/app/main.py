from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.telegram.webhook import router as telegram_router
from app.routes import agents, properties, auth, public_properties, gpt, dashboard_insights

app = FastAPI(title="InvestMateAI")

# הגדרת OAuth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# רישום ראוטרים
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard_insights.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(public_properties.router)
app.include_router(gpt.router)
app.include_router(telegram_router)

# CORS – מאפשר תקשורת בין פרונט לבאקנד בזמן פיתוח
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # אפשר להחליף לכתובת של הפרונט
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.on_event("startup")
def on_startup():
    create_tables()
