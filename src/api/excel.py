from fastapi import APIRouter, Request

from src.api.responses import excel_parser_responses
from src.schemas.excel import ShopItemsResponse
from src.services.excel import ExcelService

exel_router = APIRouter(
    prefix="/excel",
    tags=["Excel"]
)


@exel_router.get(
    path="/shop",
    response_model=ShopItemsResponse,
    summary="Возвращает все актуальные данные магазина",
    description="""
    Возвращает все актуальные данные магазина:
    
    - Делает аутентификацию пользователя по jwt;
    - Получает данные из excel таблицы;
    """,
    responses=excel_parser_responses
)
async def shop_parser(
        request: Request
):
    return await ExcelService.parse_shop(request)
