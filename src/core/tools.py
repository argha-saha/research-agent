from datetime import datetime
from ddgs import DDGS
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from core.exports import export_research, ResearchExporter
from models.research_response import ResearchResponse


def save_to_format(data: str, format_type: str = "txt", filename: str = None) -> str:
    """Save research data to specified format"""
    try:
        research_data = ResearchResponse(
            topic="Research Query",
            result=data,
            sources=[],
            tools_used=[]
        )
        return export_research(research_data, format_type)
    except Exception as e:
        return f"Export error: {str(e)}"


def save_to_txt(data: str, filename: str = "research_response.txt") -> str:
    """Legacy function for backward compatibility"""
    return save_to_format(data, "txt", filename)


def search_web(query: str) -> str:
    """Search the web using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if results:
                return "\n\n".join([f"{result['title']}: {result['body']}" for result in results])
            else:
                return "No search results found."
    except Exception as e:
        return f"Search error: {str(e)}"


save_tool = Tool(
    name="save_to_txt",
    func=save_to_txt,
    description="Save the data to a text file"
)

save_json_tool = Tool(
    name="save_to_json",
    func=lambda data: save_to_format(data, "json"),
    description="Save the data to a JSON file"
)

save_markdown_tool = Tool(
    name="save_to_markdown",
    func=lambda data: save_to_format(data, "markdown"),
    description="Save the data to a Markdown file"
)

search_tool = Tool(
    name="search",
    func=search_web,
    description="Search the web for information using DuckDuckGo"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)