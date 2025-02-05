import json
import os

from fastapi import HTTPException, status, Request
from pandas import read_excel

from src.schemas.excel import ShopItemsResponse
from src.utils.auth import verify_user_by_jwt


class ExcelService:

    @staticmethod
    async def parse_shop(request: Request):
        # user = await verify_user_by_jwt(request)
        # if not user:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        file_path = os.path.join("data", str(os.environ["PLAYIT_TABLE_FILE_NAME"]))

        if not file_path.endswith(".xlsx" or ".xls"):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable content")

        exel_shop_df = read_excel(file_path, sheet_name="Магазин")
        if not exel_shop_df:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой таблицы не существует")

        json_data = exel_shop_df.to_json(orient="records")

        formatted_json_data = json.loads(json_data)
        if not formatted_json_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Ошибка при форматировании данных из таблицы")

        return ShopItemsResponse(status=status.HTTP_200_OK, details="Данные получены", data=formatted_json_data)
