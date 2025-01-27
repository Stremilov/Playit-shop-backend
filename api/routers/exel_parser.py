import json
import os
from fastapi import APIRouter, HTTPException
from pandas import read_excel

exel_parser_router = APIRouter()


@exel_parser_router.get("/shop", response_model=list[dict])
def shop_parser():

    file_path = os.path.join("data", str(os.environ["PLAYIT_TABLE_FILE_NAME"]))

    if not file_path.endswith(".xlsx" or ".xls"):
        raise HTTPException(status_code=422, detail="Unprocessable content")

    exel_shop_df = read_excel(file_path, sheet_name="Магазин")

    json_data = exel_shop_df.to_json(orient="records")
    formated_json_data = json.loads(json_data)

    return formated_json_data
