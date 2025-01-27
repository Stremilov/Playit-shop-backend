from fastapi import FastAPI
from dotenv import load_dotenv

from api.routers.exel_parser import exel_parser_router

load_dotenv()

app = FastAPI()

app.include_router(exel_parser_router, prefix="/api/exel_parser", tags=["parsers"])

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)