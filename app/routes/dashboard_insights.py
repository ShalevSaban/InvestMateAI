from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.utils.auth_deps import get_current_agent
from app.database import get_db
from app.models import Agent
from app.services.dashboard_insights import *

# router = APIRouter(prefix="/api/dashboard")
router = APIRouter()


@router.get("/insights")
def get_dashboard_insights(
        current_agent: Agent = Depends(get_current_agent),
        db: Session = Depends(get_db)
):
    insights = {
        "top_questions": get_faqs(current_agent.id, db),
        "peak_hours": get_peak_hours(current_agent.id, db),
        "popular_properties": get_popular_properties(current_agent.id, db),
        "gpt_recommendations": get_strategy_suggestions(current_agent.id, db),
    }
    return JSONResponse(content=insights)
