from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from ddgs import DDGS

def save_to_txt(data: str, filename: str="research_response.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    formatted_text = f"Research Response -- Timestamp: {timestamp}\n\n{data}"
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)
        
    return f"Data saved to {filename}"


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

search_tool = Tool(
    name="search",
    func=search_web,
    description="Search the web for information using DuckDuckGo"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)