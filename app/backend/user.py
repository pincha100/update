
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from backend.db_depends import get_db  # Подключение к БД
from models import User  # Модель пользователя
from schemas import CreateUser, UpdateUser  # Pydantic-схемы

# Создание маршрутизатора
router = APIRouter(prefix="/users", tags=["Users"])

# --- 1. Получение всех пользователей ---
@router.get("/", summary="Получить всех пользователей")
def all_users(db: Annotated[Session, Depends(get_db)]):
    stmt = select(User)
    users = db.scalars(stmt).all()
    return users

# --- 2. Получение пользователя по ID ---
@router.get("/{user_id}", summary="Получить пользователя по ID")
def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.id == user_id)
    user = db.scalars(stmt).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

# --- 3. Создание пользователя ---
@router.post("/create", summary="Создать пользователя")
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(user.username)  # Генерация slug
    stmt = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

# --- 4. Обновление пользователя ---
@router.put("/update/{user_id}", summary="Обновить пользователя")
def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(
            firstname=user.firstname,
            lastname=user.lastname,
            age=user.age
        )
    )
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

# --- 5. Удаление пользователя ---
@router.delete("/delete/{user_id}", summary="Удалить пользователя")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User has been deleted successfully!"}

# --- 6. Задачи пользователя ---
@router.get("/{user_id}/tasks", summary="Получить задачи пользователя по ID")
def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.user_id == user_id)
    tasks = db.scalars(stmt).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")
    return tasks

# --- 5. Удаление пользователя (с удалением задач) ---
@router.delete("/delete/{user_id}", summary="Удалить пользователя")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Удаление задач, связанных с пользователем
    delete_tasks_stmt = delete(Task).where(Task.user_id == user_id)
    db.execute(delete_tasks_stmt)

    # Удаление пользователя
    delete_user_stmt = delete(User).where(User.id == user_id)
    result = db.execute(delete_user_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User and associated tasks have been deleted successfully!"}
