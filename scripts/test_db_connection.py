from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("✅ Connection to the database is successful.")
    except Exception as e:
        print("❌ Failed to connect to the database:")
        print(e)
