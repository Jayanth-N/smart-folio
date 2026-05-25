import yfinance as yf
from typing import Optional, Dict, Any
from functools import lru_cache
import time

# Cache for stock data (symbol -> (timestamp, data))
_price_cache: Dict[str, tuple] = {}
_info_cache: Dict[str, tuple] = {}
CACHE_TTL = 300  # 5 minutes


def get_current_price(symbol: str) -> Optional[float]:
    """Get current stock price with caching."""
    now = time.time()

    # Check cache
    if symbol in _price_cache:
        timestamp, price = _price_cache[symbol]
        if now - timestamp < CACHE_TTL:
            return price

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            _price_cache[symbol] = (now, price)
            return price
    except Exception:
        pass

    return None


def get_stock_info(symbol: str) -> Optional[Dict[str, Any]]:
    """Get comprehensive stock information."""
    now = time.time()

    # Check cache
    if symbol in _info_cache:
        timestamp, info = _info_cache[symbol]
        if now - timestamp < CACHE_TTL:
            return info

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1d")

        if not info or not hist.empty:
            current_price = float(hist['Close'].iloc[-1]) if not hist.empty else info.get('currentPrice', 0)

            result = {
                "symbol": symbol.upper(),
                "name": info.get("shortName", info.get("longName", symbol)),
                "current_price": current_price,
                "previous_close": info.get("previousClose", 0),
                "open_price": info.get("open", 0),
                "day_high": info.get("dayHigh", 0),
                "day_low": info.get("dayLow", 0),
                "volume": info.get("volume", 0),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "week_52_high": info.get("fiftyTwoWeekHigh", 0),
                "week_52_low": info.get("fiftyTwoWeekLow", 0),
                "beta": info.get("beta"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
            }

            _info_cache[symbol] = (now, result)
            return result

    except Exception:
        pass

    return None


def get_stock_sector(symbol: str) -> Optional[str]:
    """Get stock sector."""
    info = get_stock_info(symbol)
    return info.get("sector") if info else None


def get_stock_beta(symbol: str) -> Optional[float]:
    """Get stock beta (volatility measure)."""
    info = get_stock_info(symbol)
    return info.get("beta") if info else None
