# 🧠 InvestMateAI – Smart Real Estate AI Platform

**InvestMateAI** is a smart real estate platform built with a modular FastAPI backend. It empowers real estate agents to manage property listings, while clients can search properties using natural language via an AI-powered chat interface. The system intelligently translates questions into database queries and returns personalized property recommendations.

## 👥 System Overview

- **Real Estate Agents** can register, manage their properties, and upload images.
- **Clients** can chat naturally with the AI to discover properties based on filters like price, location, and number of rooms.
- Clients may choose to explore properties listed by a specific agent or from all available listings.
- When a property is created without a specified rental estimate or yield, **GPT-4 Turbo automatically estimates these values** based on location, price, and features.
- A **dedicated agent dashboard** provides:
  - Most frequently asked questions
  - Popular properties and peak inquiry hours
  - GPT-generated sales insights to improve conversion

## 🧱 Tech Stack & Features

- ⚙️ **FastAPI** – Python-based framework with automatic Swagger docs
- 🐘 **PostgreSQL** – Relational database with UUID keys
- 🐳 **Docker & Docker Compose** – Containerized environment
- 🔐 **JWT Authentication** – Role-based agent access and Swagger/Postman compatibility
- ☁️ **AWS S3 Integration** – Secure image uploads for property listings
- 🤖 **GPT-4 Turbo** – Natural language understanding, automatic rent/yield estimation, smart insights
- 📦 **Clean Modular Architecture** – Models, schemas, services, routes, utils
- 📊 **Dashboard Insights** – Real-time GPT-based analytics for agents

## 🗂 Project Structure

```
app/
├── main.py              # Application entry point
├── database.py          # Database connection
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic input/output schemas
├── services/            # Core business logic
├── routes/              # API routes
└── utils/               # Helpers (JWT, AWS, GPT)
```

## 🔌 API Documentation

Access the live API docs here:  
[➡️ Swagger UI](investmateai.onrender.com/docs)

## 🚀 Getting Started

```bash
# Build Docker containers
docker-compose build

# Start services
docker-compose up -d

# Apply database migrations
docker-compose exec web alembic upgrade head
```

## ✅ Current Features

- Agent authentication and CRUD operations
- Property creation with optional GPT-based enrichment (rent and yield auto-estimation)
- Client-side smart property search via GPT-4 Turbo
- Secure file/image uploads to AWS S3
- Agent dashboard with GPT-driven analytics and actionable insights
