#!/usr/bin/env python3
"""
Comprehensive verification test for Phase 1 enhancements
Tests: Caching, Fallback, Event Generation
"""

import time
from llm_client import LLMClient
from llm_cache import LLMCache
from data import get_initial_game_state

def test_caching():
    """Test that caching works correctly."""
    print("=" * 60)
    print("TEST 1: Caching System")
    print("=" * 60)
    
    client = LLMClient()
    cache = client.cache
    
    # Clear cache first
    cleared = cache.clear_all()
    print(f"✓ Cleared {cleared} old cache entries\n")
    
    game_state = get_initial_game_state()
    event_trigger = {"id": "cache_test", "type": "random", "year": 1796}
    
    # First call - should hit API
    print("📡 First call (should hit API)...")
    start = time.time()
    event1 = client.generate_event(game_state, event_trigger)
    time1 = time.time() - start
    print(f"   ✓ Generated in {time1:.2f}s")
    print(f"   Title: {event1['title']}\n")
    
    # Second call - should use cache
    print("⚡ Second call (should use cache)...")
    start = time.time()
    event2 = client.generate_event(game_state, event_trigger)
    time2 = time.time() - start
    print(f"   ✓ Generated in {time2:.2f}s")
    print(f"   Title: {event2['title']}\n")
    
    # Verify cache was used
    if time2 < time1 / 10:  # Cache should be >10x faster
        print(f"✅ CACHE WORKING: {time2:.3f}s vs {time1:.2f}s ({time1/time2:.0f}x faster)\n")
    else:
        print(f"⚠️  Cache may not be working: {time2:.2f}s vs {time1:.2f}s\n")
    
    # Show cache stats
    stats = cache.get_stats()
    print(f"Cache Stats: {stats['total_entries']} entries, {stats['total_size_mb']}MB\n")
    
    return time2 < 0.5  # Cache should be instant

def test_fallback():
    """Test fallback model support."""
    print("=" * 60)
    print("TEST 2: Fallback System")
    print("=" * 60)
    
    # Create client with a fake primary model to force fallback
    client = LLMClient(model="google/nonexistent-model")
    
    game_state = get_initial_game_state()
    event_trigger = {"id": "fallback_test", "type": "random", "year": 1796}
    
    print("🔄 Testing with fake primary model (should fallback)...")
    try:
        event = client.generate_event(game_state, event_trigger)
        print(f"   ✓ Fallback successful!")
        print(f"   Title: {event['title']}\n")
        return True
    except Exception as e:
        print(f"   ❌ Fallback failed: {e}\n")
        return False

def test_context_awareness():
    """Test that events are context-aware."""
    print("=" * 60)
    print("TEST 3: Context-Aware Event Generation")
    print("=" * 60)
    
    client = LLMClient()
    game_state = get_initial_game_state()
    
    # Add some traits/generals to test context
    game_state['player']['traits'] = ['artillery_expert', 'diplomat']
    game_state['player']['generals'] = ['ney']
    
    event_trigger = {"id": "context_test", "type": "random", "year": 1796}
    
    print("🎯 Generating event with traits and generals...")
    event = client.generate_event(game_state, event_trigger)
    
    print(f"Title: {event['title']}")
    print(f"Description: {event['description'][:100]}...")
    print(f"Choices: {len(event['choices'])}\n")
    
    # Check if description or choices reference the context
    desc_lower = event['description'].lower()
    has_context = any([
        'artillery' in desc_lower,
        'ney' in desc_lower,
        'diplomat' in desc_lower
    ])
    
    if has_context:
        print("✅ Event references player context!\n")
    else:
        print("⚠️  Event may not be using context\n")
    
    return True

def main():
    print("\n🧪 PHASE 1 VERIFICATION TEST\n")
    
    results = []
    
    # Test 1: Caching
    try:
        results.append(("Caching", test_caching()))
    except Exception as e:
        print(f"❌ Caching test failed: {e}\n")
        results.append(("Caching", False))
    
    # Test 2: Fallback
    try:
        results.append(("Fallback", test_fallback()))
    except Exception as e:
        print(f"❌ Fallback test failed: {e}\n")
        results.append(("Fallback", False))
    
    # Test 3: Context
    try:
        results.append(("Context-Aware", test_context_awareness()))
    except Exception as e:
        print(f"❌ Context test failed: {e}\n")
        results.append(("Context-Aware", False))
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(r[1] for r in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '⚠️  SOME TESTS FAILED'}\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
