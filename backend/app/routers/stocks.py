from fastapi import APIRouter, HTTPException, status, Depends

from ..auth import get_current_user
from ..schemas import StockInfo
from ..services.stock_service import get_stock_info
from ..services.risk_service import suggest_risk_level

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("/{symbol}", response_model=StockInfo)
async def get_stock(
    symbol: str,
    current_user: str = Depends(get_current_user)
):
    """Get stock information and metrics."""
    info = get_stock_info(symbol.upper())

    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {symbol} not found or data unavailable"
        )

    risk_suggestion = suggest_risk_level(symbol.upper())

    return StockInfo(
        symbol=info["symbol"],
        name=info["name"],
        current_price=info["current_price"],
        previous_close=info["previous_close"],
        open_price=info["open_price"],
        day_high=info["day_high"],
        day_low=info["day_low"],
        volume=info["volume"],
        market_cap=info.get("market_cap"),
        pe_ratio=info.get("pe_ratio"),
        dividend_yield=info.get("dividend_yield"),
        week_52_high=info["week_52_high"],
        week_52_low=info["week_52_low"],
        beta=info.get("beta"),
        sector=info.get("sector"),
        industry=info.get("industry"),
        suggested_risk=risk_suggestion["suggested_risk"]
    )


@router.get("/{symbol}/risk-suggestion")
async def get_risk_suggestion(
    symbol: str,
    current_user: str = Depends(get_current_user)
):
    """Get detailed risk suggestion for a stock."""
    suggestion = suggest_risk_level(symbol.upper())
    return {
        "symbol": symbol.upper(),
        **suggestion
    }
