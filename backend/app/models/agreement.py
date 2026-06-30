from pydantic import BaseModel


class PriceAgreement(BaseModel):
    score: float
    difference_percent: float
    providers: int
    status: str


class Agreement(BaseModel):
    price: PriceAgreement