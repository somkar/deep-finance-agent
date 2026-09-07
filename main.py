import os

import yfinance as yf
from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")


def initialize_ollama() -> ChatOllama:
    return ChatOllama(
        model="llama3.1:8b",
        temperature=0.0,
    )


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
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    return TavilySearch(max_results=5)


def build_system_prompt() -> str:
    return """
    You are a financial assistant.

    Your job is to research publicly traded companies and produce evidence-based financial reports.

    Use the available tools whenever current or structured information is needed. Do not guess financial numbers.
    If the information is not available, respond with "I don't know".

    For complex requests:
    1. Break the request into smaller sub-questions.
    2. Gather relevant information using the tools.
    3. Analyze and compare the information.
    4. Clearly distinguish between facts and your analysis.
    5. Provide a concise, well-structured final response that addresses the original request.
    """


def main() -> None:
    tools = [
        initialize_tavily_search(),
        get_company_sector,
        get_company_financials,
    ]

    task = """
    Analyze Microsoft (MSFT).

    Find:
    1. The company's latest available revenue.
    2. Its revenue growth.
    3. Its main business segments.
    4. Any significant recent company developments.

    Use the available tools to gather information and provide a concise, evidence-based report.
    Clearly distinguish between facts and your analysis. If any information is not available, respond with "I don't know".
    """

    deep_agent = create_deep_agent(
        model=initialize_ollama(),
        tools=tools,
        system_prompt=build_system_prompt(),
    )

    result = deep_agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    last_message = result["messages"][-1]
    print(getattr(last_message, "content", str(last_message)))


if __name__ == "__main__":
    main()