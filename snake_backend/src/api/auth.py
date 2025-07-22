from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from src.api.models import UserCreate, UserLogin, UserResponse, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib
import uuid

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# In-memory "user DB" for demonstration
user_db: Dict[str, Dict] = {}
session_tokens: Dict[str, str] = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def fake_hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str):
    user = user_db.get(username)
    if not user:
        return None
    if user['password_hash'] != fake_hash_password(password):
        return None
    return user

# PUBLIC_INTERFACE
@router.post("/register", response_model=UserResponse, summary="Register new user")
def register_user(data: UserCreate):
    if data.username in user_db:
        raise HTTPException(status_code=409, detail="Username already taken.")
    user_id = len(user_db) + 1
    user_db[data.username] = {
        "id": user_id,
        "username": data.username,
        "password_hash": fake_hash_password(data.password)
    }
    return UserResponse(id=user_id, username=data.username)

# PUBLIC_INTERFACE
@router.post("/login", response_model=Token, summary="User login")
def login_user(data: UserLogin):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = str(uuid.uuid4())
    session_tokens[token] = user['username']
    return Token(access_token=token)

# PUBLIC_INTERFACE
@router.post("/token", response_model=Token, summary="OAuth2 login")
def login_oauth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    session_tokens[token] = user['username']
    return Token(access_token=token, token_type="bearer")

# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = session_tokens.get(token)
    if not username or username not in user_db:
        raise HTTPException(status_code=401, detail="Invalid session token")
    user = user_db[username]
    return UserResponse(id=user["id"], username=user["username"])
