from pydantic import BaseModel


class ShopItemsResponse(BaseModel):
    status: int
    details: str
    data: dict
