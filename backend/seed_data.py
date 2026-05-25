#!/usr/bin/env python3
"""
Seed script to populate the database with sample holdings.
Run this after starting the server for the first time.
"""
import sys
import os
from datetime import date, timedelta
import random

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Holding

# Create tables
Base.metadata.create_all(bind=engine)

# Sample holdings data
SAMPLE_HOLDINGS = [
    {"symbol": "AAPL", "quantity": 50, "purchase_price": 175.50, "risk_level": "Medium"},
    {"symbol": "NVDA", "quantity": 25, "purchase_price": 450.00, "risk_level": "High"},
    {"symbol": "MSFT", "quantity": 40, "purchase_price": 380.25, "risk_level": "Medium"},
    {"symbol": "TSLA", "quantity": 15, "purchase_price": 245.00, "risk_level": "High"},
    {"symbol": "JNJ", "quantity": 60, "purchase_price": 160.75, "risk_level": "Low"},
    {"symbol": "PG", "quantity": 45, "purchase_price": 155.00, "risk_level": "Low"},
    {"symbol": "GOOGL", "quantity": 20, "purchase_price": 140.50, "risk_level": "Medium"},
    {"symbol": "AMD", "quantity": 30, "purchase_price": 120.00, "risk_level": "High"},
    {"symbol": "KO", "quantity": 80, "purchase_price": 60.25, "risk_level": "Low"},
    {"symbol": "V", "quantity": 35, "purchase_price": 275.00, "risk_level": "Medium"},
]

def seed_database(username: str = "demo"):
    """Seed the database with sample holdings for a user."""
    db = SessionLocal()

    try:
        # Check if user already has holdings
        existing = db.query(Holding).filter(Holding.username == username).count()
        if existing > 0:
            print(f"User '{username}' already has {existing} holdings. Skipping seed.")
            return

        # Add sample holdings
        for holding_data in SAMPLE_HOLDINGS:
            # Random purchase date within last year
            days_ago = random.randint(30, 365)
            purchase_date = date.today() - timedelta(days=days_ago)

            holding = Holding(
                username=username,
                symbol=holding_data["symbol"],
                quantity=holding_data["quantity"],
                purchase_price=holding_data["purchase_price"],
                purchase_date=purchase_date,
                risk_level=holding_data["risk_level"]
            )
            db.add(holding)

        db.commit()
        print(f"Successfully seeded {len(SAMPLE_HOLDINGS)} holdings for user '{username}'")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Seed for both demo users
    seed_database("demo")
    seed_database("jayanth")
    print("\nDatabase seeded successfully!")
    print("You can now login with:")
    print("  - demo / demo123")
    print("  - jayanth / password123")
