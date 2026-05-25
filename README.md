# Smart Folio

A web application for intelligent stock portfolio management with risk-based distribution recommendations, analyst insights, and clear visualizations.

## Features

- **Portfolio Management**: Add, edit, and delete stock holdings with automatic price fetching
- **Risk Categorization**: System suggests risk levels based on sector and volatility; user makes final decision
- **Recommendation Engine**: Three portfolio strategies (Aggressive, Balanced, Conservative) with rationale
- **Visualizations**: Risk distribution pie chart, sector allocation chart, and gap analysis
- **Real-time Data**: Stock prices and metrics fetched via Yahoo Finance

## Tech Stack

- **Backend**: Python (FastAPI) + SQLite
- **Frontend**: React + Vite + Tailwind CSS
- **Charts**: Recharts
- **Stock Data**: yfinance

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed sample data (optional)
python seed_data.py

# Start server
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at http://localhost:5173

## Default Credentials

- **demo** / demo123
- **jayanth** / password123

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Login, get JWT token |
| GET | /portfolio/holdings | Get user's holdings |
| POST | /portfolio/holdings | Add new holding |
| PUT | /portfolio/holdings/{id} | Update holding |
| DELETE | /portfolio/holdings/{id} | Remove holding |
| GET | /portfolio/distribution | Get risk/sector distribution |
| GET | /stocks/{symbol} | Get stock info + metrics |
| GET | /stocks/{symbol}/risk-suggestion | Get risk suggestion |
| GET | /recommendations | Get 3 strategy recommendations |

## Project Structure

```
smart-folio/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── auth.py              # JWT authentication
│   │   ├── users.json           # User credentials
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # SQLite connection
│   │   ├── routers/             # API routes
│   │   └── services/            # Business logic
│   ├── requirements.txt
│   └── seed_data.py
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/api.js      # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Risk Levels

The system suggests risk levels based on:
- **Sector**: Technology = High, Utilities = Low, etc.
- **Beta**: Higher volatility = Higher risk

Target allocation: 25% High, 25% Medium, 50% Low

**Important**: The user always has final control over risk assignment.

## License

MIT
