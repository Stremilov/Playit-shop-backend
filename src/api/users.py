from fastapi import APIRouter

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post("/points", response_model=list[dict])
def change_user_points():

    return [{"status": True}]
