from dotenv import load_dotenv
from research_agent import ResearchAgent

def main():
    load_dotenv()
    
    agent = ResearchAgent()
    
    try:
        result = agent.research_interactive()
        print(result)
    except Exception as e:
        print(f"Research failed: {e}")


if __name__ == "__main__":
    main()