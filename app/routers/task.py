from fastapi import APIRouter

router = APIRouter(
    prefix="/task",
    tags=["task"]
)

@router.get("/")
def all_tasks():
    return {"message": "All tasks"}

@router.get("/task_id")
def task_by_id():
    return {"message": "Task by ID"}

@router.post("/create")
def create_task():
    return {"message": "Task created"}

@router.put("/update")
def update_task():
    return {"message": "Task updated"}

@router.delete("/delete")
def delete_task():
    return {"message": "Task deleted"}
