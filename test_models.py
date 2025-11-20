#!/usr/bin/env python3
"""
Test which models are actually being used
"""

import subprocess
from llm_client import LLMClient
from data import get_initial_game_state

def test_direct_model_call(model):
    """Test a model directly with opencode."""
    print(f"Testing {model}...")
    try:
        result = subprocess.run(
            ["opencode", "run", "Say 'Hello from MODEL_NAME'", "--model", model],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            print(f"  ✅ {model}: {result.stdout.strip()[:60]}...")
            return True
        else:
            print(f"  ❌ {model}: {result.stderr[:60]}...")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  {model}: Timeout")
        return False
    except Exception as e:
        print(f"  ❌ {model}: {str(e)[:60]}...")
        return False

def test_llm_client_with_logging():
    """Test LLM client and show which model responds."""
    print("\n" + "="*60)
    print("Testing LLM Client Fallback Chain")
    print("="*60)
    
    client = LLMClient()
    game_state = get_initial_game_state()
    
    print(f"\nConfigured models:")
    print(f"  Primary: {client.model}")
    for i, model in enumerate(client.fallback_models, 1):
        print(f"  Fallback {i}: {model}")
    
    print(f"\n🔄 Generating event (will show which model responds)...\n")
    
    event_trigger = {"id": "model_test", "type": "random", "year": 1796}
    
    try:
        event = client.generate_event(game_state, event_trigger)
        print(f"✅ Event generated successfully!")
        print(f"   Title: {event['title']}")
        
        # Check cache to see which model was used
        cache_stats = client.cache.get_stats()
        print(f"\n📊 Cache now has {cache_stats['total_entries']} entries")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

def main():
    print("\n🧪 MODEL USAGE TEST\n")
    
    # Test 1: Direct model calls
    print("="*60)
    print("TEST 1: Direct Model Availability")
    print("="*60)
    
    models = [
        "google/gemini-2.0-flash",
        "google/gemini-2.5-flash", 
        "google/gemini-flash-latest"
    ]
    
    for model in models:
        test_direct_model_call(model)
    
    # Test 2: LLM client
    test_llm_client_with_logging()
    
    print("\n" + "="*60)
    print("✅ Test Complete")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
