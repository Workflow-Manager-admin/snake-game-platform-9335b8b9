from fastapi import APIRouter
from src.api.models import ScoreEntry, LeaderboardResponse

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"]
)

# In-memory store for demonstration only
mock_leaderboard = [
    {"username": "alice", "score": 52},
    {"username": "bob", "score": 40},
    {"username": "carol", "score": 36},
    {"username": "guest", "score": 10},
]

# PUBLIC_INTERFACE
@router.get("/", response_model=LeaderboardResponse, summary="Get global leaderboard")
def get_leaderboard():
    """
    Returns the top scores across all users.
    """
    results = sorted(mock_leaderboard, key=lambda k: k["score"], reverse=True)[:10]
    return LeaderboardResponse(leaderboard=[ScoreEntry(**entry) for entry in results])
