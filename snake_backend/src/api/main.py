from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth import router as auth_router
from src.api.game import router as game_router
from src.api.leaderboard import router as leaderboard_router

openapi_tags = [
    {"name": "Authentication", "description": "User registration, login, and session management."},
    {"name": "Gameplay", "description": "Snake game logic: start game, make a move, etc."},
    {"name": "Leaderboard", "description": "High scores and leaderboard display."}
]

app = FastAPI(
    title="Snake Game Backend API",
    description="Backend service for Snake game: Play the game, track scores, manage users and retrieve the leaderboard.",
    version="0.1.0",
    openapi_tags=openapi_tags
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Utility"])
def health_check():
    """Returns health status for the backend API."""
    return {"message": "Healthy"}

# Register API routers
app.include_router(auth_router)
app.include_router(game_router)
app.include_router(leaderboard_router)
