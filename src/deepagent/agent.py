from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

from .config import OLLAMA_MODEL
from .prompts import RESEARCH_TASK, SYSTEM_PROMPT
from .tools import get_company_financials, get_company_sector, initialize_tavily_search


def initialize_ollama() -> ChatOllama:
    return ChatOllama(model=OLLAMA_MODEL, temperature=0.0)


def run_agent() -> str:
    tools = [
        initialize_tavily_search(),
        get_company_sector,
        get_company_financials,
    ]
    deep_agent = create_deep_agent(
        model=initialize_ollama(),
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
    result = deep_agent.invoke({"messages": [{"role": "user", "content": RESEARCH_TASK}]})
    last_message = result["messages"][-1]
    return getattr(last_message, "content", str(last_message))
