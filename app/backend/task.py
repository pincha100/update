from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from backend.db_depends import get_db  # Подключение к БД
from models import Task, User  # Модели задач и пользователей
from schemas import CreateTask, UpdateTask  # Pydantic-схемы

# Создание маршрутизатора
router = APIRouter(prefix="/tasks", tags=["Tasks"])


# --- 1. Получение всех задач ---
@router.get("/", summary="Получить все задачи")
def all_tasks(db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task)
    tasks = db.scalars(stmt).all()
    return tasks


# --- 2. Получение задачи по ID ---
@router.get("/{task_id}", summary="Получить задачу по ID")
def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.id == task_id)
    task = db.scalars(stmt).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task


# --- 3. Создание задачи ---
@router.post("/create", summary="Создать задачу")
def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Проверка существования пользователя
    user_stmt = select(User).where(User.id == user_id)
    user = db.scalars(user_stmt).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Создание задачи
    slug = slugify(task.title)  # Генерация slug
    stmt = insert(Task).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=task.completed,
        user_id=user_id,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


# --- 4. Обновление задачи ---
@router.put("/update/{task_id}", summary="Обновить задачу")
def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(
            title=task.title,
            content=task.content,
            priority=task.priority,
            completed=task.completed
        )
    )
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task was not found")
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}


# --- 5. Удаление задачи ---
@router.delete("/delete/{task_id}", summary="Удалить задачу")
def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(Task).where(Task.id == task_id)
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task was not found")
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task has been deleted successfully!"}
