from datetime import date, datetime

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import verify_password
from models.task import Task
from models.user import User


async def get_tasks(db: AsyncSession, owner_id: int):
    tasks = await db.execute(select(Task).filter(Task.owner_id == owner_id))
    return tasks.scalars().all()


async def get_task(db: AsyncSession, task_id: int, owner_id: int):
    task = await db.execute(select(Task).filter(
        Task.id == task_id,
        Task.owner_id == owner_id))
    return task.scalar_one_or_none()


async def create_task(db: AsyncSession,
                      title: str,
                      description: str,
                      priority: int,
                      due_date: date,
                      completed: bool,
                      owner_id: int):
    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        completed=completed,
        owner_id=owner_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession,
                      task_id: int,
                      title: str,
                      description: str,
                      priority: int,
                      due_date: date,
                      completed: bool,
                      owner_id: int):
    task = await get_task(db, task_id, owner_id)
    if not task:
        return None
    task.title = title
    task.description = description
    task.priority = priority
    task.due_date = due_date
    task.completed = completed
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int, owner_id: int):
    task = await get_task(db, task_id, owner_id)
    if not task:
        return None
    await db.delete(task)
    await db.commit()
    return task


async def create_user(
        db: AsyncSession,
        username: str,
        email: str,
        password: str):
    hash = pbkdf2_sha256.hash(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hash,
        created_at=datetime.now())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, username: str):
    user = await db.execute(select(User).filter(User.username == username))
    if user:
        return user.scalar_one_or_none()
    return None


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
