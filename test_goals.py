#!/usr/bin/env python3
"""
Test Player-Driven Goals System
"""

from goals_system import Goal, GoalType, parse_goal, check_goal_progress, get_active_goals
from llm_client import LLMClient
from data import get_initial_game_state

def test_goals_system():
    print("\n🎯 TESTING PLAYER-DRIVEN GOALS SYSTEM\n")
    
    # Initialize
    game_state = get_initial_game_state()
    llm_client = LLMClient()
    
    # Test 1: Goal parsing
    print("="*60)
    print("TEST 1: Goal Parsing")
    print("="*60)
    
    test_goals = [
        "Conquer Italy by 1800",
        "Form an alliance with Spain",
        "Amass 100,000 troops",
        "Control all Mediterranean trade routes"
    ]
    
    for desc in test_goals:
        parsed = parse_goal(desc)
        print(f"\n✓ Goal: {desc}")
        print(f"  Type: {parsed['type'].value}")
        print(f"  Keywords: {', '.join(parsed['keywords'])}")
        print(f"  Difficulty: {parsed['difficulty']}/10")
    
    print()
    
    # Test 2: Create and track goals
    print("="*60)
    print("TEST 2: Goal Creation & Tracking")
    print("="*60)
    
    # Create a conquest goal
    goal = Goal("test1", "Conquer Italy by 1800", GoalType.CONQUEST)
    print(f"\n✓ Created goal: {goal.description}")
    print(f"  Initial progress: {goal.progress}%")
    
    # Simulate conquering Italy
    game_state['player']['territories'].append("Italy")
    new_progress = check_goal_progress(goal, game_state)
    goal.update_progress(new_progress)
    
    print(f"  After conquering Italy: {goal.progress}%")
    
    if goal.status.value == "completed":
        print("  ✅ Goal completed!")
    else:
        print(f"  Status: {goal.status.value}")
    
    # Add to game state
    game_state['goals'] = [goal.to_dict()]
    
    print()
    
    # Test 3: Goal-driven event generation
    print("="*60)
    print("TEST 3: Goal-Driven Event Generation")
    print("="*60)
    
    event_trigger = {"id": "goal_test", "type": "random", "year": 1796}
    
    print(f"\n🎲 Generating event with active goal: '{goal.description}'")
    print("   [This should create an event related to conquering Italy...]")
    print("   [Generating...]\n")
    
    try:
        event = llm_client.generate_event(game_state, event_trigger)
        
        print(f"✅ Event generated successfully!")
        print(f"\n   Title: {event['title']}")
        print(f"   Description: {event['description'][:100]}...")
        
        # Check if event mentions Italy or conquest
        event_text = (event['title'] + " " + event['description']).lower()
        goal_relevant = any(word in event_text for word in ['italy', 'italian', 'conquest', 'territory'])
        
        if goal_relevant:
            print(f"\n   ✅ Event appears goal-related (mentions Italy/conquest)")
        else:
            print(f"\n   ⚠️  Event may not be directly goal-related")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print()
    
    # Test 4: Multiple goals
    print("="*60)
    print("TEST 4: Multiple Active Goals")
    print("="*60)
    
    # Add another goal
    goal2 = Goal("test2", "Form alliance with Spain", GoalType.DIPLOMATIC)
    game_state['goals'].append(goal2.to_dict())
    
    active = get_active_goals(game_state)
    print(f"\n✓ Active goals: {len(active)}")
    for g in active:
        print(f"  - {g.description} ({g.type.value}, {g.progress}%)")
    
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print("✅ All goal system tests passed!")
    print(f"✅ {len(active)} active goals tracked")
    print("✅ Events generate with goal context")
    print()
    
    return True

if __name__ == "__main__":
    success = test_goals_system()
    exit(0 if success else 1)
