from typing import List, Dict, Any, Optional
from sessions.session_manager import SessionManager


def display_sessions_list(sessions: List[Dict[str, Any]]) -> None:
    if not sessions:
        print("No research sessions found.")
        return
    
    print("\n" + "=" * 17)
    print("Research Sessions")
    print("=" * 17)
    print(f"{'ID':<4} {'Topic':<40} {'Model':<20} {'Entries':<8} {'Updated':<20}")
    print("-" * 17)
    
    for session in sessions:
        topic = session['topic'][:40] + "..." if len(session['topic']) > 43 else session['topic']
        print(f"{session['id']:<4} {topic:<44} {session['model_used']} "
              f"{session.get('entry_count', 0):<8} {session['updated_at'][:19]:<20}")


def display_session_details(session: Dict[str, Any], entries: List[Dict[str, Any]]) -> None:
    print("\n" + "=" * 43)
    print(f"Session Details - ID: {session['id']}")
    print("=" * 43)
    print(f"Topic: {session['topic']}")
    print(f"Model: {session['model_used']}")
    print(f"Status: {session['status']}")
    print(f"Created: {session['created_at']}")
    print(f"Updated: {session['updated_at']}")
    print(f"Total Entries: {len(entries)}")
    
    if entries:
        print("\nResearch Entries:")
        print("-" * 43)
        for i, entry in enumerate(entries, 1):
            print(f"\n{i}. Query: {entry['query']}")
            print(f"   Result: {entry['result'][:100]}...")
            print(f"   Sources: {len(entry['sources'])} sources")
            print(f"   Tools: {', '.join(entry['tools_used'])}")
            print(f"   Timestamp: {entry['timestamp']}")


def prompt_for_session_selection(sessions: List[Dict[str, Any]]) -> Optional[int]:
    if not sessions:
        return None
    
    while True:
        try:
            choice = input(f"\nEnter session ID (1-{len(sessions)}): ").strip()
            session_id = int(choice)
            
            # Check if session ID exists
            if any(session['id'] == session_id for session in sessions):
                return session_id
            else:
                print(f"Invalid session ID. Please choose from the list above.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nSelection cancelled.")
            return None