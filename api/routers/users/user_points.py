from fastapi import APIRouter, HTTPException

user_points_router = APIRouter()

@user_points_router.post("/points", response_model=list[dict])
def change_user_points():

    return [{"status": True}]
