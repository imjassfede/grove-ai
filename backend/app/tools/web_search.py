from langchain_core.tools import tool


@tool
async def web_search(query: str) -> str:
    """Search the web for current information about a topic."""
    # TODO: integrate a search provider (Tavily, Brave, etc.)
    raise NotImplementedError
