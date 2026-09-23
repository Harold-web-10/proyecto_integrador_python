from app.core.security import create_access_token, verify_password
from app.crud.user import user_crud
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    **Iniciar sesión** — devuelve un token JWT.

    - **username**: nombre de usuario o correo electrónico
    - **password**: contraseña del usuario

    ## Respuestas
    - **200**: Token JWT válido
    - **401**: Credenciales inválidas
    """
    user = user_crud.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta está inactiva.",
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login-json", response_model=Token)
def login_json(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> Token:
    """
    **Iniciar sesión vía JSON** — alternativa a ``/login`` para clientes que
    no pueden enviar form-data.

    ## Respuestas
    - **200**: Token JWT válido
    - **401**: Credenciales inválidas
    """
    user = user_crud.authenticate(db, payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta está inactiva.",
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> UserRead:
    """
    **Registrar nuevo usuario**.

    El primer usuario registrado automáticamente obtiene el rol de **admin**.
    Los siguientes usuarios registrados obtienen el rol de **user**.
    """
    existing = user_crud.get_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo electrónico.",
        )
    existing = user_crud.get_by_username(db, payload.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese nombre de usuario.",
        )

    from app.core.enums import UserRole

    user_count = user_crud.get_multi(db, limit=1)
    role = UserRole.ADMIN if not user_count else UserRole.USER

    user = user_crud.create(db, payload, role=role)
    return UserRead.model_validate(user)
