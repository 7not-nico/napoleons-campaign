"""
NPC Dialogue Handler for main.py
"""

from npc_system import create_npc_instance, get_available_npcs, get_npc
from ui import show_available_npcs, show_npc_dialogue
from rich.prompt import Prompt


def handle_npc_dialogue(game_state):
    """Handle NPC dialogue interaction."""
    from llm_client import LLMClient
    
    # Initialize NPCs if needed
    if 'npcs' not in game_state:
        game_state['npcs'] = {}
    
    while True:
        show_available_npcs(game_state)
        
        npc_choice = Prompt.ask("[bold]Talk to[/bold]").lower()
        
        if npc_choice == "back" or npc_choice == "":
            break
            
        # Check if NPC is available
        available_ids = get_available_npcs(game_state)
        if npc_choice not in available_ids:
            print(f"[yellow]'{npc_choice}' is not available.[/yellow]\n")
            continue
            
        # Create NPC instance if first time
        if npc_choice not in game_state['npcs']:
            npc = create_npc_instance(npc_choice)
            if npc:
                game_state['npcs'][npc_choice] = npc.to_dict()
            else:
                continue
        
        # Load NPC from game state
        from npc_system import NPC
        npc = NPC.from_dict(game_state['npcs'][npc_choice])
        
        # Get player input
        player_input = Prompt.ask(f"\n[bold cyan]You say to {npc.name}[/bold cyan]")
        
        if not player_input or player_input.lower() == "back":
            break
        
        # Generate response
        llm_client = game_state.get('llm_client')
        if not llm_client:
            llm_client = LLMClient()
            game_state['llm_client'] = llm_client
        
        print("\n[dim]Thinking...[/dim]")
        dialogue_data = llm_client.generate_npc_dialogue(npc, game_state, player_input)
        
        # Update relationship
        relationship_change = dialogue_data.get('relationship_change', 0)
        npc.add_conversation(player_input, dialogue_data['response'], relationship_change)
        
        # Save updated NPC
        game_state['npcs'][npc_choice] = npc.to_dict()
        
        # Show response
        show_npc_dialogue(npc, dialogue_data['response'], npc.relationship, relationship_change)
        
        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
