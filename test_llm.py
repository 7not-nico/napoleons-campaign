#!/usr/bin/env python3
"""
Test script for LLM integration with opencode/zen
"""

from llm_client import LLMClient
from data import get_initial_game_state

def test_llm_generation():
    print("🧪 Testing OpenCode Zen LLM Integration...\n")
    
    # Initialize LLM client
    client = LLMClient()
    print(f"✓ LLM Client initialized with model: {client.model}\n")
    
    # Create a test game state
    game_state = get_initial_game_state()
    print(f"✓ Game state created:")
    print(f"  Year: {game_state['year']}")
    print(f"  Troops: {game_state['player']['troops']:,}")
    print(f"  Gold: {game_state['player']['gold']:,}")
    print(f"  Morale: {game_state['player']['morale']}")
    print()
    
    # Create event trigger
    event_trigger = {
        "id": "test_event",
        "type": "random",
        "year": 1796
    }
    
    print("🎲 Generating random event with OpenCode Zen...")
    print("This may take a moment...\n")
    
    try:
        event = client.generate_event(game_state, event_trigger)
        
        print("✅ Event generated successfully!\n")
        print("=" * 60)
        print(f"Title: {event['title']}")
        print(f"Type: {event['type']}")
        print(f"\nDescription:")
        print(event['description'])
        print(f"\nChoices:")
        for i, choice in enumerate(event['choices'], 1):
            print(f"\n  {i}. {choice['text']}")
            if choice.get('consequences'):
                print(f"     Consequences: {choice['consequences']}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: Make sure you're authenticated with opencode.")
        print("Run: opencode auth login")
        return False

if __name__ == "__main__":
    success = test_llm_generation()
    exit(0 if success else 1)
