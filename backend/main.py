from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.market_data import MarketDataService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the AlphaSight API!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/analyze/{ticker}")
async def analyze_stock(ticker: str):
    market_data_service = MarketDataService()
    company_overview = await market_data_service.get_company_overview(ticker)

    if company_overview is None:
        raise HTTPException(status_code=404, detail="Ticker not found")

    return company_overview