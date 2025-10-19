from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.utils.auth_deps import get_current_agent
from app.models import Agent

router = APIRouter(prefix="/cleanup", tags=["Cleanup"])


@router.delete("/old-tables")
def delete_old_tables(
        confirm: str,
        current_agent: Agent = Depends(get_current_agent),
        db: Session = Depends(get_db)
):
    """
    Delete old PostgreSQL tables that moved to Redis.

    Usage: DELETE /cleanup/old-tables?confirm=YES_DELETE_EVERYTHING
    """

    if confirm != "YES_DELETE_EVERYTHING":
        raise HTTPException(
            status_code=400,
            detail="Must confirm with: confirm=YES_DELETE_EVERYTHING"
        )

    try:
        # Drop tables
        db.execute(text("DROP TABLE IF EXISTS messages CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS conversations CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS cached_criteria CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS insight_logs CASCADE"))
        db.commit()

        return {
            "message": "Old tables deleted successfully",
            "deleted_tables": [
                "messages",
                "conversations",
                "cached_criteria",
                "insight_logs"
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


@router.delete("/old-data-only")
def delete_old_data_only(
        confirm: str,
        current_agent: Agent = Depends(get_current_agent),
        db: Session = Depends(get_db)
):
    """
    Delete only data from old tables (keep structure).

    Usage: DELETE /cleanup/old-data-only?confirm=YES_DELETE_DATA
    """

    if confirm != "YES_DELETE_DATA":
        raise HTTPException(
            status_code=400,
            detail="Must confirm with: confirm=YES_DELETE_DATA"
        )

    try:
        # Check if tables exist
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('messages', 'conversations', 'cached_criteria', 'insight_logs')
        """))

        existing_tables = [row[0] for row in result]

        if not existing_tables:
            return {
                "message": "No old tables found - already clean!",
                "existing_tables": []
            }

        deleted_counts = {}

        # Delete data from each table
        for table in existing_tables:
            result = db.execute(text(f"DELETE FROM {table}"))
            deleted_counts[table] = result.rowcount

        db.commit()

        return {
            "message": "Old data deleted successfully",
            "deleted_counts": deleted_counts,
            "note": "Tables still exist (empty)"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


@router.get("/status")
def check_cleanup_status(db: Session = Depends(get_db)):
    """Check which old tables still exist."""

    try:
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('messages', 'conversations', 'cached_criteria', 'insight_logs')
        """))

        existing_tables = [row[0] for row in result]

        # Count rows in each table
        counts = {}
        for table in existing_tables:
            count_result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
            counts[table] = count_result.scalar()

        return {
            "status": "clean" if not existing_tables else "needs_cleanup",
            "existing_old_tables": existing_tables,
            "row_counts": counts,
            "recommendation": "Delete with /cleanup/old-tables?confirm=YES_DELETE_EVERYTHING" if existing_tables else "Already clean!"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }