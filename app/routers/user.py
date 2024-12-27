from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/")
def all_users():
    return {"message": "All users"}

@router.get("/user_id")
def user_by_id():
    return {"message": "User by ID"}

@router.post("/create")
def create_user():
    return {"message": "User created"}

@router.put("/update")
def update_user():
    return {"message": "User updated"}

@router.delete("/delete")
def delete_user():
    return {"message": "User deleted"}
