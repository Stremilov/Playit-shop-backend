import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from src.api.routers import all_routers


load_dotenv()


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger("shop_logger")


app = FastAPI(root_path="/playit/shop")


for router in all_routers:
    app.include_router(router)


async def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
