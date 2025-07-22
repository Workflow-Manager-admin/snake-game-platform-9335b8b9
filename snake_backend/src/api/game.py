from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Optional
import random
import uuid
from src.api.models import (
    GameStartRequest,
    GameMoveRequest,
    GameMoveResponse,
    SnakeState,
)
from src.api.auth import get_current_user, UserResponse

router = APIRouter(
    prefix="/game",
    tags=["Gameplay"]
)

BOARD_SIZE = 20
INITIAL_SNAKE_LEN = 3

# In-memory temporary sessions (replace with DB/Redis for production)
game_sessions: Dict[str, Dict] = {}

def get_random_food(coord_exclude: List[List[int]]) -> List[int]:
    while True:
        fx, fy = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
        if [fx, fy] not in coord_exclude:
            return [fx, fy]

def next_snake_position(snake, direction):
    head = snake[0][:]
    if direction == "up":
        head[1] -= 1
    elif direction == "down":
        head[1] += 1
    elif direction == "left":
        head[0] -= 1
    elif direction == "right":
        head[0] += 1
    return head

# PUBLIC_INTERFACE
@router.post("/start", response_model=SnakeState, summary="Start new Snake game")
def start_game(data: GameStartRequest, current_user: Optional[UserResponse] = Depends(get_current_user)):
    """
    Starts a new Snake game and returns the initial board state.
    """
    snake = [[BOARD_SIZE // 2, BOARD_SIZE // 2 + i] for i in range(INITIAL_SNAKE_LEN)]
    food = get_random_food(snake)
    session_id = str(uuid.uuid4())
    game_sessions[session_id] = {
        "snake": snake,
        "food": food,
        "direction": "up",
        "score": 0,
        "is_alive": True,
        "username": current_user.username if current_user else None,
    }
    return SnakeState(score=0, snake=snake, food=food, direction="up", is_alive=True)

# PUBLIC_INTERFACE
@router.post("/move", response_model=GameMoveResponse, summary="Send move and update Snake game state")
def move_snake(move: GameMoveRequest, current_user: Optional[UserResponse] = Depends(get_current_user)):
    """
    Updates the snake's position given a direction.
    (For simplicity, uses a fake per-user game state and is not persistent.)
    """
    # Find the user's current game state or return 404
    username = current_user.username if current_user else None
    session = None
    for s in game_sessions.values():
        if s.get('username', None) == username:
            session = s
            break
    if not session:
        raise HTTPException(status_code=404, detail="No ongoing game session for user.")
    if not session["is_alive"]:
        raise HTTPException(status_code=410, detail="Game is over. Start a new game.")

    snake = session["snake"]
    food = session["food"]
    direction = move.direction
    new_head = next_snake_position(snake, direction)
    # Check boundaries
    if not (0 <= new_head[0] < BOARD_SIZE and 0 <= new_head[1] < BOARD_SIZE):
        session["is_alive"] = False
        return GameMoveResponse(state=SnakeState(
            score=session["score"], snake=snake, food=food, direction=direction, is_alive=False
        ))
    # Check collision with self
    if new_head in snake:
        session["is_alive"] = False
        return GameMoveResponse(state=SnakeState(
            score=session["score"], snake=snake, food=food, direction=direction, is_alive=False
        ))
    # Move snake
    snake.insert(0, new_head)
    if new_head == food:
        session["score"] += 1
        session["food"] = get_random_food(snake)
    else:
        snake.pop()
    session["snake"] = snake
    session["direction"] = direction

    return GameMoveResponse(state=SnakeState(
        score=session["score"], snake=snake, food=session["food"], direction=direction, is_alive=session["is_alive"]
    ))
