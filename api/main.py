from fastapi import FastAPI
from dotenv import load_dotenv

from api.routers.exel.exel_parser import exel_parser_router
from api.routers.users.user_points import user_points_router

load_dotenv()


app = FastAPI()

app.include_router(exel_parser_router, prefix="/api/exel/parser", tags=["exel"])
app.include_router(user_points_router, prefix="/api/users", tags=["users"])

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)