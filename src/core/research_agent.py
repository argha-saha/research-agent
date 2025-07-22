from core.agent_config import get_tools, create_agent, create_agent_executor
from core.llm_config import create_openai_llm, create_parser, create_prompt
from models.research_response import ResearchResponse

class ResearchAgent:
    def __init__(self, model: str = "gpt-4o", verbose: bool = False):
        """Initialize the research agent with specified model and verbose setting"""
        self.llm = create_openai_llm(model)
        self.parser = create_parser()
        self.prompt = create_prompt(self.parser)
        self.tools = get_tools()
        self.agent = create_agent(self.llm, self.prompt, self.tools)
        self.agent_executor = create_agent_executor(self.agent, self.tools, verbose=verbose)
    
    
    def research(self, query: str) -> ResearchResponse:
        """Perform research on the given query"""
        try:
            raw_response = self.agent_executor.invoke({"query": query})
            structured_response = self.parser.parse(raw_response.get("output"))
            return structured_response
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Raw response: {raw_response}")
            raise
    
    
    def research_interactive(self) -> ResearchResponse:
        query = input("Ask: ")
        return self.research(query) 