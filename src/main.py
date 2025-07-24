import argparse
from dotenv import load_dotenv
from core.research_agent import ResearchAgent
from core.exports import ResearchExporter, export_research
from sessions.session_manager import SessionManager
from sessions.session_commands import (
    handle_list_sessions, handle_load_session, handle_delete_session, 
    handle_new_session, display_session_details
)

def parse_arguments() -> argparse.Namespace:
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
  python src/main.py --export pdf       # Export results to PDF
  python src/main.py --export all       # Export to all formats
  
Session Management:
  python src/main.py --new-session --session-topic "CPU Architecture"
  python src/main.py --history
  python src/main.py --load 2
  python src/main.py --delete 4
  python src/main.py --model o3
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
    
    parser.add_argument(
        "--export", "-e",
        choices=["txt", "json", "markdown", "pdf", "all"],
        help="Export research results to specified format(s)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="exports",
        help="Directory to save exported files (default: exports)"
    )
    
    # Session management arguments
    parser.add_argument(
        "--new-session",
        action="store_true",
        help="Start a new research session"
    )
    
    parser.add_argument(
        "--session-topic",
        help="Topic for new session (required with --new-session)"
    )
    
    parser.add_argument(
        "--history",
        action="store_true",
        help="List recent research sessions"
    )
    
    parser.add_argument(
        "--load",
        type=int,
        help="Load a specific session by ID"
    )
    
    parser.add_argument(
        "--delete",
        type=int,
        help="Delete a specific session by ID"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="LLM model to use"
    )
    
    return parser.parse_args()


def print_status(args) -> None:
    print("AI Research Agent")
    print("-" * 17)
    
    if args.verbose:
        print("✓ Verbose mode enabled")
        
    if args.tools:
        print("✓ Tools display enabled")
        
    if args.export:
        print(f"✓ Export mode: {args.export}")
        print(f"✓ Output directory: {args.output_dir}")
        
    if args.new_session:
        print(f"✓ New session: {args.session_topic}")
        
    if args.history:
        print("✓ Session history mode")
        
    if args.load:
        print(f"✓ Load session: {args.load}")
        
    if args.delete:
        print(f"✓ Delete session: {args.delete}")
        
    if args.model:
        print(f"✓ Model: {args.model}")
        
    if not any([args.verbose, args.tools]):
        print("✓ Clean output mode (results and sources only)")
        
    print()


def export_results(research_result, export_format: str, output_dir: str) -> None:
    """Export research results to specified format(s)"""
    exporter = ResearchExporter(output_dir)
    
    if export_format == "all":
        results = exporter.export_all(research_result)
        print("\n" + "=" * 14)
        print("Export Results")
        print("=" * 14)
        for fmt, filepath in results.items():
            if filepath.startswith("Error:"):
                print(f"✗ {fmt.upper()}: {filepath}")
            else:
                print(f"✓ {fmt.upper()}: {filepath}")
    else:
        try:
            filepath = export_research(research_result, export_format, output_dir)
            print(f"\n✓ Exported to: {filepath}")
        except Exception as e:
            print(f"\n✗ Export failed: {e}")


def main() -> None:
    args = parse_arguments()
    
    if args.all:
        args.verbose = True
        args.tools = True
    
    print_status(args)
    
    load_dotenv()
    
    # Intialize session manager
    session_manager = SessionManager()
    
    # Handle session management commands
    if args.new_session:
        if not args.session_topic:
            # TODO: Auto-generate a topic based on query instead of requiring user to provide one
            print("Error: --session-topic is required with --new-session")
            return
        if not handle_new_session(session_manager, args.session_topic, args.model):
            return
        
    if args.history:
        handle_list_sessions(session_manager)
        return
    
    if args.delete:
        handle_delete_session(session_manager, args.delete)
        return
    
    if args.load:
        if not handle_load_session(session_manager, args.load):
            return
    
    # Initialize research agent
    agent = ResearchAgent(model=args.model, verbose=args.verbose, session_manager=session_manager)
    
    # If no session is active, create one
    if not session_manager.is_session_active():
        topic = input("Enter research topic: ").strip()
        if topic:
            session_manager.create_new_session(topic, args.model)
            print(f"✓ Created new session: {topic}")
        else:
            print("No topic provided.")
            return
    
    try:
        result = agent.research_interactive()
        
        print("\n" + "=" * 16)
        print("Research Results")
        print("=" * 16)
        print(result.result)
        print(f"\nSources: {result.sources}")
        
        if args.tools:
            print(f"\nTools used: {result.tools_used}")
        
        if args.export:
            export_results(result, args.export, args.output_dir)
            
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.")
    except Exception as e:
        print(f"\nResearch failed: {e}")


if __name__ == "__main__":
    main()