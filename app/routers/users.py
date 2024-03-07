from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, SecretStr, Field

from fastapi import APIRouter, Depends, HTTPException


from sql_app import crud, schemas
from sqlalchemy.orm import Session
from sql_app.database import get_db

from LogManager import logger


from pprint import pprint

# from ..dependencies import get_token_header

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# ================== login ==================


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Test endpoint:
    curl -X POST -H "content-type: application/x-www-form-urlencoded" \
        "http://169.254.53.100:8081/users/token" \
        -d "username=alice" -d "password=password123"
    """

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            # NOTE: additional token information added here
        },
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# @router.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user


@router.get("/me/items")
async def read_own_items(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    """
    Example:
        curl -X POST -H "content-type: application/x-www-form-urlencoded" "http://10.8.0.22:8081/users/token" -d "username=alice" -d "password=password123"
        curl -X GET -H "Authorization: Bearer <token>" "http://10.8.0.22:8081/users/me/items/"
    """

    return [{"item_id": "Foo", "owner": current_user.username}]


# ================== Register User ==================
# class UserCreate(BaseModel):
#     """
#     input model
#     """

#     username: str
#     email: EmailStr
#     password: SecretStr


# class UserInDB(UserCreate):
#     hashed_password: str
#     created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
#     is_active: bool = True
#     is_locked: bool = False
#     is_verified: bool = False
#     last_failed_login: datetime | None = None
#     last_login: datetime | None = None
#     last_update_at: datetime | None = None
#     password_changed_at: datetime | None = None
#     reset_token: str | None = None
#     reset_token_expires_at: datetime | None = None
#     role: str = Field(default_factory=lambda: "user")
#     two_factor_enabled: bool = Field(default=False)
#     two_factor_secret: str | None = None


# class User(BaseModel):
#     """
#     output model
#     """

#     username: str
#     email: EmailStr
#     is_active: bool
#     is_locked: bool


# def create_user(user: UserCreate):
#     print(f"{user.dict()=}")
#     print(f"{user.password.get_secret_value()=}")
#     hashed_password = get_password_hash(user.password.get_secret_value())

#     db_user = UserInDB(**user.dict(), hashed_password=hashed_password)
#     fake_users_db[user.username] = db_user.dict()

#     pprint(fake_users_db)
#     return db_user


# @router.post("/register", response_model=User)
# async def register_user(user: UserCreate):
#     print("!!!!!! Register_user !!!!!!!")
#     # print(user)
#     if user.username in fake_users_db:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     return create_user(user).dict()


# @router.get("/me/", response_model=schemas.User)
# async def read_users_me(
#     current_user: Annotated[schemas.User, Depends(get_current_active_user)]
# ):
#     return current_user


# @router.get("/delete/", response_model=schemas.User)
# async def delete_user(
#     current_user: Annotated[schemas.User, Depends(get_current_active_user)]
# ):
#     return crud.delete_user(db=db, user_id=current_user.id)
