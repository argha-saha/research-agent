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
        topic = (
            session["topic"][:40] + "..."
            if len(session["topic"]) > 43
            else session["topic"]
        )
        print(
            f"{session['id']:<4} {topic:<44} {session['model_used']} "
            f"{session.get('entry_count', 0):<8} {session['updated_at'][:19]:<20}"
        )


def display_session_details(
    session: Dict[str, Any], entries: List[Dict[str, Any]]
) -> None:
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
            if any(session["id"] == session_id for session in sessions):
                return session_id
            else:
                print(f"Invalid session ID. Please choose from the list above.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nSelection cancelled.")
            return None


def confirm_action(action: str) -> bool:
    while True:
        response = input(f"\n{action} (y/n): ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no", ""]:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def handle_list_sessions(session_manager: SessionManager, limit: int = 10) -> None:
    """Handle the --history command"""
    sessions = session_manager.list_recent_sessions(limit)

    # Add entry count to each session
    for session in sessions:
        entries = session_manager.db.get_session_entries(session["id"])
        session["entry_count"] = len(entries)

    display_sessions_list(sessions)


def handle_load_session(session_manager: SessionManager, session_id: int) -> bool:
    """Handle the --load command"""
    if session_manager.load_session(session_id):
        session_data = session_manager.get_current_session()
        entries = session_manager.get_current_session_entries()

        print(f"\n✓ Loaded session {session_id}: {session_data['topic']}")
        print(f"  Entries: {len(entries)}")
        print(f"  Model: {session_data['model_used']}")

        if entries:
            print(f"  Last query: {entries[-1]['query']}")

        return True
    else:
        print(f"\n✗ Session {session_id} not found.")
        return False


def handle_delete_session(session_manager: SessionManager, session_id: int) -> bool:
    """Handle the --delete command"""
    session_data = session_manager.db.get_session(session_id)
    if not session_data:
        print(f"\n✗ Session {session_id} not found.")
        return False

    print(f"\nSession to delete:")
    print(f"  ID: {session_data['id']}")
    print(f"  Topic: {session_data['topic']}")
    print(f"  Created: {session_data['created_at']}")
    print(f"  Model: {session_data['model_used']}")

    if confirm_action("Are you sure you want to delete this session?"):
        if session_manager.delete_session(session_id):
            print(f"\n✓ Session {session_id} deleted successfully.")
            return True
        else:
            print(f"\n✗ Failed to delete session {session_id}.")
            return False
    else:
        print("\nDeletion cancelled.")
        return False


def handle_new_session(session_manager: SessionManager, topic: str, model: str) -> bool:
    """Handle the --new-session command"""
    if session_manager.is_session_active():
        current = session_manager.get_current_session()
        print(f"\nCurrent session active: {current['topic']} (ID: {current['id']})")

        if not confirm_action(
            "Do you want to close the current session and start a new one?"
        ):
            return False

    session_id = session_manager.create_new_session(topic, model)
    print(f"\n✓ Created new session {session_id}: {topic}")
    print(f"  Model: {model}")

    return True