from langchain_core.tools import tool


@tool
async def summarize_data(data: dict) -> str:
    """Summarize structured data into key insights."""
    # TODO: implement data summarization logic
    raise NotImplementedError
