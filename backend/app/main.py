from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth, portfolio, stocks, recommendations

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Folio API",
    description="Stock Portfolio Management with Risk-Based Recommendations",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(stocks.router)
app.include_router(recommendations.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Welcome to Smart Folio API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
