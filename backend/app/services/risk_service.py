from typing import Optional
from .stock_service import get_stock_info

# Sector risk mapping
SECTOR_RISK = {
    # High risk sectors
    "Technology": "High",
    "Consumer Cyclical": "High",
    "Communication Services": "High",

    # Medium risk sectors
    "Financial Services": "Medium",
    "Healthcare": "Medium",
    "Industrials": "Medium",
    "Basic Materials": "Medium",
    "Energy": "Medium",

    # Low risk sectors
    "Consumer Defensive": "Low",
    "Utilities": "Low",
    "Real Estate": "Low",
}

# Default risk by beta
def get_risk_by_beta(beta: Optional[float]) -> str:
    """Determine risk level based on beta value."""
    if beta is None:
        return "Medium"
    if beta > 1.3:
        return "High"
    elif beta > 0.8:
        return "Medium"
    else:
        return "Low"


def suggest_risk_level(symbol: str) -> dict:
    """
    Suggest risk level for a stock based on sector and volatility.
    Returns suggested risk level and the factors considered.
    """
    info = get_stock_info(symbol)

    if not info:
        return {
            "suggested_risk": "Medium",
            "confidence": "low",
            "factors": {
                "sector": None,
                "sector_risk": None,
                "beta": None,
                "beta_risk": None
            },
            "rationale": "Unable to fetch stock data. Defaulting to Medium risk."
        }

    sector = info.get("sector")
    beta = info.get("beta")

    sector_risk = SECTOR_RISK.get(sector, "Medium")
    beta_risk = get_risk_by_beta(beta)

    # Combine sector and beta for final suggestion
    risk_scores = {"High": 3, "Medium": 2, "Low": 1}
    avg_score = (risk_scores[sector_risk] + risk_scores[beta_risk]) / 2

    if avg_score >= 2.5:
        suggested_risk = "High"
    elif avg_score >= 1.5:
        suggested_risk = "Medium"
    else:
        suggested_risk = "Low"

    # Build rationale
    rationale_parts = []
    if sector:
        rationale_parts.append(f"Sector ({sector}) suggests {sector_risk} risk")
    if beta:
        rationale_parts.append(f"Beta of {beta:.2f} indicates {beta_risk} volatility")

    return {
        "suggested_risk": suggested_risk,
        "confidence": "high" if sector and beta else "medium",
        "factors": {
            "sector": sector,
            "sector_risk": sector_risk,
            "beta": beta,
            "beta_risk": beta_risk
        },
        "rationale": ". ".join(rationale_parts) if rationale_parts else "Based on available data."
    }
