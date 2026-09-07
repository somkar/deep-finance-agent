import os

import yfinance as yf
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from .config import require_tavily_api_key


@tool(description="Return the industry sector for a company name.")
def get_company_sector(company_name: str) -> str:
    """Return the sector for a given company."""
    company_sectors = {
        "Apple": "Technology",
        "Microsoft": "Technology",
        "JP Morgan": "Financial Services",
        "Tesla": "Automotive",
    }
    return company_sectors.get(
        company_name,
        f"Sector information for {company_name} is not available.",
    )


@tool(description="Return the financials for a company given its ticker symbol.")
def get_company_financials(ticker: str) -> dict:
    """Return key financial metrics for a company ticker."""
    company = yf.Ticker(ticker)
    info = company.info

    return {
        "company": info.get("longName", "N/A"),
        "ticker": ticker.upper(),
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "revenue": info.get("totalRevenue", "N/A"),
        "gross_profit": info.get("grossProfits", "N/A"),
        "operating_income": info.get("operatingIncome", "N/A"),
        "net_income": info.get("netIncome", "N/A"),
        "profit_margin": info.get("profitMargins", "N/A"),
        "revenue_growth": info.get("revenueGrowth", "N/A"),
        "return_on_equity": info.get("returnOnEquity", "N/A"),
    }


def initialize_tavily_search() -> TavilySearch:
    os.environ["TAVILY_API_KEY"] = require_tavily_api_key()
    return TavilySearch(max_results=5)
