from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3
import os

app = FastAPI()

DB_PATH = "reviews.db"


class ReviewIn(BaseModel):
    text: str


class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str


POSITIVE_WORDS = ["хорош", "люблю", "нравит", "отличн", "супер", "класс", "удобн"]
NEGATIVE_WORDS = ["плохо", "ненавиж", "ужас", "неудоб", "бесит", "туп", "глюч"]


def detect_sentiment(text: str) -> str:
    text = text.lower()
    if any(word in text for word in POSITIVE_WORDS):
        return "positive"
    if any(word in text for word in NEGATIVE_WORDS):
        return "negative"
    return "neutral"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        ''')


init_db()


@app.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewIn):
    sentiment = detect_sentiment(review.text)
    created_at = datetime.utcnow().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
            (review.text, sentiment, created_at)
        )
        review_id = cursor.lastrowid

    return {
        "id": review_id,
        "text": review.text,
        "sentiment": sentiment,
        "created_at": created_at
    }


@app.get("/reviews", response_model=List[ReviewResponse])
def get_reviews(sentiment: Optional[str] = Query(None)):
    query = "SELECT id, text, sentiment, created_at FROM reviews"
    params = []

    if sentiment:
        query += " WHERE sentiment = ?"
        params.append(sentiment)

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]
