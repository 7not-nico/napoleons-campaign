#!/usr/bin/env python3
"""
Test NPC Dialogue System
"""

from npc_system import create_npc_instance, get_available_npcs
from llm_client import LLMClient
from data import get_initial_game_state

def test_npc_dialogue():
    print("\n🎭 TESTING NPC DIALOGUE SYSTEM\n")
    
    # Initialize
    game_state = get_initial_game_state()
    game_state['player']['generals'] = ['ney']  # Add Ney as available
    
    llm_client = LLMClient()
    
    # Test 1: Available NPCs
    print("="*60)
    print("TEST 1: Available NPCs")
    print("="*60)
    
    available = get_available_npcs(game_state)
    print(f"✓ Available NPCs: {', '.join(available)}")
    print()
    
    # Test 2: Create NPC instance
    print("="*60)
    print("TEST 2: Create NPC Instance")
    print("="*60)
    
    npc = create_npc_instance('ney')
    if npc:
        print(f"✓ Created: {npc.name}")
        print(f"  Role: {npc.role}")
        print(f"  Personality: {npc.personality[:60]}...")
        print(f"  Relationship: {npc.relationship}/100")
    else:
        print("❌ Failed to create NPC")
        return False
    print()
    
    # Test 3: Generate dialogue
    print("="*60)
    print("TEST 3: Generate Dialogue")
    print("="*60)
    
    test_inputs = [
        "What do you think about our current situation?",
        "Should we attack or defend?"
    ]
    
    for player_input in test_inputs:
        print(f"\n💬 You: \"{player_input}\"")
        print("   [Generating response...]")
        
        try:
            dialogue_data = llm_client.generate_npc_dialogue(npc, game_state, player_input)
            
            response = dialogue_data['response']
            rel_change = dialogue_data['relationship_change']
            
            print(f"\n   {npc.name}: \"{response}\"")
            
            # Update relationship
            old_rel = npc.relationship
            npc.add_conversation(player_input, response, rel_change)
            
            if rel_change != 0:
                arrow = "↑" if rel_change > 0 else "↓"
                print(f"   Relationship: {old_rel} → {npc.relationship} ({rel_change:+d}) {arrow}")
            else:
                print(f"   Relationship: {npc.relationship} (no change)")
                
            print("   ✅ Response generated successfully")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    # Test 4: Conversation history
    print("\n" + "="*60)
    print("TEST 4: Conversation History")
    print("="*60)
    
    history = npc.get_recent_history(5)
    print(f"✓ Stored {len(history)} conversations in memory")
    
    if history:
        print("\nRecent conversation:")
        for i, conv in enumerate(history, 1):
            print(f"  {i}. You: {conv['player'][:40]}...")
            print(f"     {npc.name}: {conv['npc'][:40]}...")
    
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print("✅ All NPC dialogue tests passed!")
    print(f"✅ Final relationship with {npc.name}: {npc.relationship}/100")
    print()
    
    return True

if __name__ == "__main__":
    success = test_npc_dialogue()
    exit(0 if success else 1)
