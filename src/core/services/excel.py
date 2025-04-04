import json

import pandas
from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pandas import read_excel

from src.core.schemas.excel import ShopItemsResponse
from src.core.utils.auth import verify_user_by_jwt


class ExcelService:

    @staticmethod
    async def parse_shop(
            request: Request,
            session: AsyncSession
    ):
        await verify_user_by_jwt(request=request, session=session)

        file_path = "PlayIT.xlsx"

        if not file_path.endswith(".xlsx" or ".xls"):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable content")

        exel_shop_df = read_excel(file_path, sheet_name="Магазин")
        if exel_shop_df.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой таблицы не существует")

        json_data = exel_shop_df.to_json(orient="records")

        formatted_json_data = json.loads(json_data)
        if not formatted_json_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Ошибка при форматировании данных из таблицы")

        return ShopItemsResponse(status=status.HTTP_200_OK, details="Данные получены", data=formatted_json_data)

    @staticmethod
    async def decrement_prize_count(request: Request, item_name: str):
        try:
            file_path = "PlayIT.xlsx"

            if not file_path.endswith((".xlsx", ".xls")):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable content")

            try:
                excel_shop_df = read_excel(file_path, sheet_name="Магазин")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка загрузки файла: {str(e)}")

            if excel_shop_df.empty:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой таблицы не существует")

            if "Наименование" not in excel_shop_df.columns or "Кол-во" not in excel_shop_df.columns:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{Некорректный формат таблицы")

            index = excel_shop_df[excel_shop_df["Наименование"] == item_name].index

            if index.empty:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")

            if excel_shop_df.at[index[0], "Кол-во"] > 0:
                excel_shop_df.at[index[0], "Кол-во"] -= 1
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Товар закончился")

            try:
                with pandas.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                    excel_shop_df.to_excel(writer, sheet_name="Магазин", index=False)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка сохранения файла: {str(e)}")

            return {"status": status.HTTP_200_OK, "message": f"Количество '{item_name}' уменьшено"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка decrement_prize_count {str(e)}")
