# Health Vitals Log

Flask + SQLAlchemy web app for logging patient vitals (heart rate, temperature, SpO2).
Uses SQLite locally and PostgreSQL on Render (via the `DATABASE_URL` environment variable).

## Run locally
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Deploy on Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Environment variable: `DATABASE_URL` = Internal Database URL of your Render PostgreSQL
