import argparse
from dotenv import load_dotenv
from core.research_agent import ResearchAgent

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AI Research Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py                    # Basic usage (clean output)
  python src/main.py --verbose          # Show detailed thought process
  python src/main.py --tools            # Show tools used
  python src/main.py --all              # Show both verbose output and tools
  python src/main.py -v -t              # Short form for verbose and tools
        """
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output to show LLM thought process"
    )
    
    parser.add_argument(
        "--tools", "-t",
        action="store_true",
        help="Show tools used during research"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Enable both verbose output and show tools (equivalent to --verbose --tools)"
    )
    
    return parser.parse_args()


def print_status(args):
    print("AI Research Agent")
    print("-" * 25)
    
    if args.verbose:
        print("✓ Verbose mode enabled")
    if args.tools:
        print("✓ Tools display enabled")
    if not args.verbose and not args.tools:
        print("✓ Clean output mode (results and sources only)")
        
    print()


def main():
    args = parse_arguments()
    
    if args.all:
        args.verbose = True
        args.tools = True
    
    print_status(args)
    
    load_dotenv()
    agent = ResearchAgent(verbose=args.verbose)
    
    try:
        result = agent.research_interactive()
        
        print("\n" + "=" * 16)
        print("Research Results")
        print("=" * 16)
        print(result.result)
        print(f"\nSources: {result.sources}")
        
        if args.tools:
            print(f"\nTools used: {result.tools_used}")
            
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.")
    except Exception as e:
        print(f"\nResearch failed: {e}")


if __name__ == "__main__":
    main()