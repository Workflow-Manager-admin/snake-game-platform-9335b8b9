from pydantic import BaseModel, Field
from typing import Optional, List

# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., description="User's unique username")
    password: str = Field(..., min_length=6, description="User's password (min 6 chars)")

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., description="User's username")
    password: str = Field(..., description="User's password")

# PUBLIC_INTERFACE
class UserResponse(BaseModel):
    """Schema for returning user info to client."""
    id: int
    username: str

# PUBLIC_INTERFACE
class Token(BaseModel):
    """Authentication token."""
    access_token: str
    token_type: str = "bearer"

# PUBLIC_INTERFACE
class GameStartRequest(BaseModel):
    """Request body for starting a new game."""
    username: Optional[str] = Field(None, description="Username of the player (optional for guests)")

# PUBLIC_INTERFACE
class SnakeState(BaseModel):
    """State of the snake game board."""
    score: int
    snake: List[List[int]]
    food: List[int]
    direction: str
    is_alive: bool

# PUBLIC_INTERFACE
class GameMoveRequest(BaseModel):
    """Request for submitting a move."""
    direction: str = Field(..., description="New direction (up, down, left, right)")

# PUBLIC_INTERFACE
class GameMoveResponse(BaseModel):
    """Updated game state after move."""
    state: SnakeState

# PUBLIC_INTERFACE
class ScoreEntry(BaseModel):
    """Leaderboard entry."""
    username: str
    score: int

# PUBLIC_INTERFACE
class LeaderboardResponse(BaseModel):
    """All-time leaderboard (top scores)."""
    leaderboard: List[ScoreEntry]
