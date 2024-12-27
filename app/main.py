from fastapi import FastAPI
from backend.user import router as user_router
from backend.task import router as task_router

app = FastAPI()

# Подключение маршрутов
app.include_router(user_router)
app.include_router(task_router)  # Добавляем маршруты для task

# Точка входа
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
