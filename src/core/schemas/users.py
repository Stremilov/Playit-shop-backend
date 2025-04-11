from pydantic import BaseModel


class ExchangeData(BaseModel):
    user_id: int
    prize_id: int
    prize_title: str
    value: int


class ExchangeResponse(BaseModel):
    status: str
    details: str
    user: dict
