from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from ..models import Holding
from ..schemas import HoldingCreate, HoldingUpdate, HoldingResponse, PortfolioDistribution, RiskDistribution, SectorDistribution
from ..services.stock_service import get_current_price, get_stock_sector

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/holdings", response_model=List[HoldingResponse])
async def get_holdings(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get all holdings for the current user with current prices."""
    holdings = db.query(Holding).filter(Holding.username == current_user).all()

    result = []
    for holding in holdings:
        current_price = get_current_price(holding.symbol)
        current_value = current_price * holding.quantity if current_price else None
        cost_basis = holding.purchase_price * holding.quantity
        gain_loss = current_value - cost_basis if current_value else None
        gain_loss_percent = (gain_loss / cost_basis * 100) if gain_loss and cost_basis else None

        result.append(HoldingResponse(
            id=holding.id,
            username=holding.username,
            symbol=holding.symbol,
            quantity=holding.quantity,
            purchase_price=holding.purchase_price,
            purchase_date=holding.purchase_date,
            risk_level=holding.risk_level,
            current_price=current_price,
            current_value=current_value,
            gain_loss=gain_loss,
            gain_loss_percent=gain_loss_percent
        ))

    return result


@router.post("/holdings", response_model=HoldingResponse, status_code=status.HTTP_201_CREATED)
async def create_holding(
    holding: HoldingCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Add a new holding to the portfolio."""
    db_holding = Holding(
        username=current_user,
        symbol=holding.symbol.upper(),
        quantity=holding.quantity,
        purchase_price=holding.purchase_price,
        purchase_date=holding.purchase_date,
        risk_level=holding.risk_level
    )
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)

    current_price = get_current_price(db_holding.symbol)
    current_value = current_price * db_holding.quantity if current_price else None
    cost_basis = db_holding.purchase_price * db_holding.quantity
    gain_loss = current_value - cost_basis if current_value else None
    gain_loss_percent = (gain_loss / cost_basis * 100) if gain_loss and cost_basis else None

    return HoldingResponse(
        id=db_holding.id,
        username=db_holding.username,
        symbol=db_holding.symbol,
        quantity=db_holding.quantity,
        purchase_price=db_holding.purchase_price,
        purchase_date=db_holding.purchase_date,
        risk_level=db_holding.risk_level,
        current_price=current_price,
        current_value=current_value,
        gain_loss=gain_loss,
        gain_loss_percent=gain_loss_percent
    )


@router.put("/holdings/{holding_id}", response_model=HoldingResponse)
async def update_holding(
    holding_id: int,
    holding_update: HoldingUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update an existing holding."""
    db_holding = db.query(Holding).filter(
        Holding.id == holding_id,
        Holding.username == current_user
    ).first()

    if not db_holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found"
        )

    update_data = holding_update.model_dump(exclude_unset=True)
    if "symbol" in update_data:
        update_data["symbol"] = update_data["symbol"].upper()

    for key, value in update_data.items():
        setattr(db_holding, key, value)

    db.commit()
    db.refresh(db_holding)

    current_price = get_current_price(db_holding.symbol)
    current_value = current_price * db_holding.quantity if current_price else None
    cost_basis = db_holding.purchase_price * db_holding.quantity
    gain_loss = current_value - cost_basis if current_value else None
    gain_loss_percent = (gain_loss / cost_basis * 100) if gain_loss and cost_basis else None

    return HoldingResponse(
        id=db_holding.id,
        username=db_holding.username,
        symbol=db_holding.symbol,
        quantity=db_holding.quantity,
        purchase_price=db_holding.purchase_price,
        purchase_date=db_holding.purchase_date,
        risk_level=db_holding.risk_level,
        current_price=current_price,
        current_value=current_value,
        gain_loss=gain_loss,
        gain_loss_percent=gain_loss_percent
    )


@router.delete("/holdings/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holding(
    holding_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete a holding from the portfolio."""
    db_holding = db.query(Holding).filter(
        Holding.id == holding_id,
        Holding.username == current_user
    ).first()

    if not db_holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found"
        )

    db.delete(db_holding)
    db.commit()
    return None


@router.get("/distribution", response_model=PortfolioDistribution)
async def get_portfolio_distribution(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get portfolio distribution by risk level and sector."""
    holdings = db.query(Holding).filter(Holding.username == current_user).all()

    if not holdings:
        return PortfolioDistribution(
            total_value=0,
            risk_distribution=[],
            sector_distribution=[],
            target_allocation={"High": 25, "Medium": 25, "Low": 50}
        )

    # Calculate values and distributions
    risk_totals = {"High": 0.0, "Medium": 0.0, "Low": 0.0}
    risk_counts = {"High": 0, "Medium": 0, "Low": 0}
    sector_totals = {}
    total_value = 0.0

    for holding in holdings:
        current_price = get_current_price(holding.symbol)
        if current_price:
            value = current_price * holding.quantity
            total_value += value
            risk_totals[holding.risk_level] += value
            risk_counts[holding.risk_level] += 1

            sector = get_stock_sector(holding.symbol) or "Unknown"
            sector_totals[sector] = sector_totals.get(sector, 0) + value

    # Build risk distribution
    risk_distribution = []
    for level in ["High", "Medium", "Low"]:
        if risk_totals[level] > 0 or risk_counts[level] > 0:
            risk_distribution.append(RiskDistribution(
                risk_level=level,
                value=risk_totals[level],
                percentage=(risk_totals[level] / total_value * 100) if total_value > 0 else 0,
                count=risk_counts[level]
            ))

    # Build sector distribution
    sector_distribution = [
        SectorDistribution(
            sector=sector,
            value=value,
            percentage=(value / total_value * 100) if total_value > 0 else 0
        )
        for sector, value in sorted(sector_totals.items(), key=lambda x: -x[1])
    ]

    return PortfolioDistribution(
        total_value=total_value,
        risk_distribution=risk_distribution,
        sector_distribution=sector_distribution,
        target_allocation={"High": 25, "Medium": 25, "Low": 50}
    )
