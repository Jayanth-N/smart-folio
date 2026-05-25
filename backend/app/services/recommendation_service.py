from typing import List, Dict, Any
from sqlalchemy.orm import Session

from ..models import Holding
from .stock_service import get_current_price, get_stock_sector


def calculate_portfolio_metrics(holdings: List[Holding]) -> Dict[str, Any]:
    """Calculate current portfolio metrics."""
    total_value = 0.0
    risk_values = {"High": 0.0, "Medium": 0.0, "Low": 0.0}
    sector_values = {}
    holding_details = []

    for holding in holdings:
        current_price = get_current_price(holding.symbol)
        if current_price:
            value = current_price * holding.quantity
            total_value += value
            risk_values[holding.risk_level] += value

            sector = get_stock_sector(holding.symbol) or "Unknown"
            sector_values[sector] = sector_values.get(sector, 0) + value

            holding_details.append({
                "symbol": holding.symbol,
                "risk_level": holding.risk_level,
                "value": value,
                "sector": sector
            })

    # Calculate percentages
    risk_percentages = {
        level: (value / total_value * 100) if total_value > 0 else 0
        for level, value in risk_values.items()
    }

    return {
        "total_value": total_value,
        "risk_values": risk_values,
        "risk_percentages": risk_percentages,
        "sector_values": sector_values,
        "holding_details": holding_details
    }


def generate_aggressive_strategy(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Generate aggressive (high-risk) strategy recommendation."""
    current = metrics["risk_percentages"]
    target = {"High": 60, "Medium": 30, "Low": 10}

    rebalance_actions = []
    total_value = metrics["total_value"]

    for holding in metrics["holding_details"]:
        symbol = holding["symbol"]
        current_pct = (holding["value"] / total_value * 100) if total_value > 0 else 0

        if holding["risk_level"] == "High":
            action = "hold" if current["High"] >= 50 else "buy"
            rationale = "Core position for aggressive growth" if action == "hold" else "Increase exposure to high-growth stocks"
        elif holding["risk_level"] == "Low":
            action = "sell" if current["Low"] > 15 else "hold"
            rationale = "Reduce defensive positions to fund growth" if action == "sell" else "Maintain minimal defensive hedge"
        else:
            action = "hold"
            rationale = "Maintain balanced exposure"

        rebalance_actions.append({
            "symbol": symbol,
            "action": action,
            "current_allocation": round(current_pct, 1),
            "target_allocation": round(current_pct * (target[holding["risk_level"]] / max(current[holding["risk_level"]], 1)), 1),
            "shares_to_trade": None,
            "rationale": rationale
        })

    return {
        "name": "Aggressive Growth",
        "risk_level": "High",
        "expected_return": "12-18% annually",
        "description": "Maximize growth potential through concentrated positions in high-growth sectors like technology and emerging markets.",
        "suggested_allocation": target,
        "rebalance_actions": rebalance_actions,
        "rationale": f"Your current portfolio has {current['High']:.1f}% in high-risk assets. "
                     f"An aggressive strategy targets 60% in high-growth positions. "
                     f"This approach suits investors with long time horizons and high risk tolerance."
    }


def generate_balanced_strategy(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Generate balanced (medium-risk) strategy recommendation."""
    current = metrics["risk_percentages"]
    target = {"High": 25, "Medium": 50, "Low": 25}

    rebalance_actions = []
    total_value = metrics["total_value"]

    for holding in metrics["holding_details"]:
        symbol = holding["symbol"]
        current_pct = (holding["value"] / total_value * 100) if total_value > 0 else 0

        if holding["risk_level"] == "Medium":
            action = "buy" if current["Medium"] < 45 else "hold"
            rationale = "Increase core balanced positions" if action == "buy" else "Maintain balanced allocation"
        elif holding["risk_level"] == "High":
            if current["High"] > 30:
                action = "sell"
                rationale = "Reduce volatility exposure"
            else:
                action = "hold"
                rationale = "Maintain growth component"
        else:
            action = "hold" if current["Low"] <= 30 else "sell"
            rationale = "Maintain stability component" if action == "hold" else "Rebalance from overly defensive"

        rebalance_actions.append({
            "symbol": symbol,
            "action": action,
            "current_allocation": round(current_pct, 1),
            "target_allocation": round(current_pct * (target[holding["risk_level"]] / max(current[holding["risk_level"]], 1)), 1),
            "shares_to_trade": None,
            "rationale": rationale
        })

    return {
        "name": "Balanced Portfolio",
        "risk_level": "Medium",
        "expected_return": "8-12% annually",
        "description": "Achieve steady growth with moderate volatility through diversified sector allocation and balanced risk exposure.",
        "suggested_allocation": target,
        "rebalance_actions": rebalance_actions,
        "rationale": f"Your current allocation is {current['High']:.1f}% high-risk, {current['Medium']:.1f}% medium, "
                     f"and {current['Low']:.1f}% low-risk. A balanced strategy targets equal growth and stability. "
                     f"Ideal for moderate risk tolerance with 5-10 year investment horizons."
    }


def generate_conservative_strategy(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Generate conservative (low-risk) strategy recommendation."""
    current = metrics["risk_percentages"]
    target = {"High": 10, "Medium": 30, "Low": 60}

    rebalance_actions = []
    total_value = metrics["total_value"]

    for holding in metrics["holding_details"]:
        symbol = holding["symbol"]
        current_pct = (holding["value"] / total_value * 100) if total_value > 0 else 0

        if holding["risk_level"] == "Low":
            action = "buy" if current["Low"] < 50 else "hold"
            rationale = "Increase defensive positions for stability" if action == "buy" else "Maintain strong defensive core"
        elif holding["risk_level"] == "High":
            action = "sell" if current["High"] > 15 else "hold"
            rationale = "Reduce exposure to volatile assets" if action == "sell" else "Maintain minimal growth exposure"
        else:
            action = "hold"
            rationale = "Maintain moderate growth component"

        rebalance_actions.append({
            "symbol": symbol,
            "action": action,
            "current_allocation": round(current_pct, 1),
            "target_allocation": round(current_pct * (target[holding["risk_level"]] / max(current[holding["risk_level"]], 1)), 1),
            "shares_to_trade": None,
            "rationale": rationale
        })

    return {
        "name": "Conservative Income",
        "risk_level": "Low",
        "expected_return": "4-8% annually",
        "description": "Prioritize capital preservation and steady income through dividend-paying blue chips and defensive sectors.",
        "suggested_allocation": target,
        "rebalance_actions": rebalance_actions,
        "rationale": f"Your portfolio currently has {current['Low']:.1f}% in low-risk assets. "
                     f"A conservative strategy prioritizes capital preservation with 60% in defensive positions. "
                     f"Best suited for risk-averse investors or those nearing financial goals."
    }


def generate_recommendations(db: Session, username: str) -> Dict[str, Any]:
    """Generate all three strategy recommendations."""
    holdings = db.query(Holding).filter(Holding.username == username).all()

    if not holdings:
        return {
            "current_distribution": {"High": 0, "Medium": 0, "Low": 0},
            "strategies": []
        }

    metrics = calculate_portfolio_metrics(holdings)

    return {
        "current_distribution": metrics["risk_percentages"],
        "strategies": [
            generate_aggressive_strategy(metrics),
            generate_balanced_strategy(metrics),
            generate_conservative_strategy(metrics)
        ]
    }
