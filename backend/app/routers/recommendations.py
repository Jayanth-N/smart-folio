from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from ..schemas import RecommendationsResponse
from ..services.recommendation_service import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=RecommendationsResponse)
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Get portfolio recommendations with 3 strategies:
    - Aggressive Growth (High Risk)
    - Balanced Portfolio (Medium Risk)
    - Conservative Income (Low Risk)

    Each strategy includes:
    - Suggested allocation percentages
    - Rebalancing actions for current holdings
    - Detailed rationale
    """
    return generate_recommendations(db, current_user)
