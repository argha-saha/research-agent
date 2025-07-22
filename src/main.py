from dotenv import load_dotenv
from core.research_agent import ResearchAgent

def main():
    load_dotenv()
    agent = ResearchAgent()
    
    try:
        result = agent.research_interactive()
        print(result.result)
        print(f"Sources: {result.sources}")
        print(f"Tools used: {result.tools_used}")
    except Exception as e:
        print(f"Research failed: {e}")


if __name__ == "__main__":
    main()