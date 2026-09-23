from app.schemas.auth import LoginRequest, Token, TokenPayload
from app.schemas.favorite import FavoriteCreate, FavoriteRead
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.work import WorkCreate, WorkRead, WorkUpdate

__all__ = [
    # Auth
    "LoginRequest",
    "Token",
    "TokenPayload",
    # User
    "UserCreate",
    "UserRead",
    "UserUpdate",
    # Work
    "WorkCreate",
    "WorkRead",
    "WorkUpdate",
    # Review
    "ReviewCreate",
    "ReviewRead",
    "ReviewUpdate",
    # Favorite
    "FavoriteCreate",
    "FavoriteRead",
]
