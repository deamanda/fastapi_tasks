from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated

import jwt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_access_token
from config import settings
from crud import (authenticate_user, create_task, create_user, delete_task,
                  get_task, get_tasks, get_user, update_task)
from database import Base, SessionLocal, engine
from schemas.task import CreatedTask, NewTask
from schemas.token import Token, TokenData
from schemas.user import User, UserSignUp


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db():
    async with SessionLocal() as db:
        yield db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()

    yield


app = FastAPI(lifespan=lifespan)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/auth/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user


@app.get("/tasks/", response_model=list[CreatedTask])
async def read_tasks(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_active_user)):
    return await get_tasks(db, user.id)


@app.get("/tasks/{task_id}", response_model=CreatedTask)
async def read_task(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_active_user)):
    task = await get_task(db, task_id, user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return task


@app.post("/tasks/", response_model=CreatedTask)
async def post_task(task: NewTask,
                    db: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_active_user)):
    return await create_task(db,
                             title=task.title,
                             description=task.description,
                             priority=task.priority,
                             due_date=task.due_date,
                             completed=task.completed,
                             owner_id=user.id)


@app.put("/tasks/{task_id}", response_model=CreatedTask)
async def put_task(task_id: int,
                   task: NewTask,
                   db: AsyncSession = Depends(get_db),
                   user: User = Depends(get_current_active_user)):
    new_task = await update_task(db=db,
                                 task_id=task_id,
                                 title=task.title,
                                 description=task.description,
                                 priority=task.priority,
                                 due_date=task.due_date,
                                 completed=task.completed,
                                 owner_id=user.id)
    if not new_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return new_task


@app.delete("/tasks/{task_id}")
async def del_task(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_active_user)):
    task = await delete_task(db, task_id, user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users/", response_model=User)
async def post_user(user: UserSignUp,
                    db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(db, user.username,
                                     user.email,
                                     user.password.get_secret_value())
        return new_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
