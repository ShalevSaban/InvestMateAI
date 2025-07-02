FROM python:3.10-slim

# סביבת עבודה
WORKDIR /app

# תלות לקומפילציה של חבילות כמו bcrypt, psycopg2, ועוד
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# התקנת תלויות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת שאר קבצי הפרויקט
COPY . .

# לוודא ש-python רואה את app/
ENV PYTHONPATH=/app

# סקריפט הרצה שכולל alembic + uvicorn
COPY start.sh .
RUN chmod +x start.sh

# פורט להפניה – תואם ל-uvicorn
EXPOSE 8000

# פקודת הרצה
CMD ["./start.sh"]
