from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.utils.auth_deps import get_current_agent
from app.database import get_db
from app.models import Agent
from app.services.dashboard_insights import *

router = APIRouter()

@router.get("/insights")
def get_dashboard_insights(
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    # Check Redis cache for GPT recommendations
    gpt_recommendation = get_cached_gpt_insight(current_agent.id, db)

    if not gpt_recommendation:
        print("🔄 No cache - generating new GPT insights")
        gpt_recommendation = get_strategy_suggestions(current_agent.id, db)
        save_gpt_insight(current_agent.id, gpt_recommendation, db)

    insights = {
        "top_questions": get_faqs(current_agent.id, db),
        "peak_hours": get_peak_hours(current_agent.id, db),
        "popular_properties": get_popular_properties(current_agent.id, db),
        "gpt_recommendations": gpt_recommendation,
        "stats": get_conversation_stats(current_agent.id)
    }

    return JSONResponse(content=insights)