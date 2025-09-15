from fastapi import FastAPI, Request
import asyncpg
from datetime import datetime

app = FastAPI()

DATABASE_URL = "postgresql://neondb_owner:npg_RcvO5wqdbMt0@ep-shiny-salad-afnmotb6-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

@app.post("/log")
async def log_data(req: Request):
    body = await req.json()
    temp = body.get("temperature")
    iso_ts = body.get("timestamp")  # ISO 8601 string from ESP32/Postman

    # Convert ISO string to datetime object
    ts = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))

    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO temperature_logs (timestamp, temperature) VALUES ($1, $2)",
        ts, temp
    )
    await conn.close()

    return {"status": "ok"}