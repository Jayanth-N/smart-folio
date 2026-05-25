from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


# Authentication schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Holding schemas
class HoldingBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10)
    quantity: float = Field(..., gt=0)
    purchase_price: float = Field(..., gt=0)
    purchase_date: date
    risk_level: str = Field(..., pattern="^(High|Medium|Low)$")


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    symbol: Optional[str] = Field(None, min_length=1, max_length=10)
    quantity: Optional[float] = Field(None, gt=0)
    purchase_price: Optional[float] = Field(None, gt=0)
    purchase_date: Optional[date] = None
    risk_level: Optional[str] = Field(None, pattern="^(High|Medium|Low)$")


class HoldingResponse(HoldingBase):
    id: int
    username: str
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    gain_loss: Optional[float] = None
    gain_loss_percent: Optional[float] = None

    class Config:
        from_attributes = True


# Stock schemas
class StockInfo(BaseModel):
    symbol: str
    name: str
    current_price: float
    previous_close: float
    open_price: float
    day_high: float
    day_low: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    week_52_high: float
    week_52_low: float
    beta: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    suggested_risk: str


# Portfolio distribution schemas
class RiskDistribution(BaseModel):
    risk_level: str
    value: float
    percentage: float
    count: int


class SectorDistribution(BaseModel):
    sector: str
    value: float
    percentage: float


class PortfolioDistribution(BaseModel):
    total_value: float
    risk_distribution: List[RiskDistribution]
    sector_distribution: List[SectorDistribution]
    target_allocation: dict


# Recommendation schemas
class RebalanceAction(BaseModel):
    symbol: str
    action: str  # "buy", "sell", "hold"
    current_allocation: float
    target_allocation: float
    shares_to_trade: Optional[float] = None
    rationale: str


class StrategyRecommendation(BaseModel):
    name: str
    risk_level: str
    expected_return: str
    description: str
    suggested_allocation: dict
    rebalance_actions: List[RebalanceAction]
    rationale: str


class RecommendationsResponse(BaseModel):
    current_distribution: dict
    strategies: List[StrategyRecommendation]
