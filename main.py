#!/usr/bin/env python3
"""
Napoleon's Campaign - A CLI Strategy Game

A text-based strategy game where you play as Napoleon Bonaparte,
making historical decisions that shape the fate of Europe.
"""

import sys
import typer
from typing import Optional
from game_logic import process_turn, check_game_over, initialize_game
from ui import (
    show_main_menu,
    show_status,
    show_event,
    get_player_choice,
    show_game_over,
    show_instructions,
    clear_screen,
    show_error_message,
    show_success_message,
    show_map,
)
from data import get_initial_game_state
from utils import save_game, load_game

# Initialize Typer app
app = typer.Typer(help="Napoleon's Campaign - A Historical Strategy Game")


def run_game_loop(game_state):
    """Main game loop handling turns and events."""
    while not game_state["game_over"]:
        clear_screen()

        # Show current game status
        show_status(game_state)

        # Process current event
        current_event = game_state["current_event"]
        if current_event:
            show_event(current_event)

            # Get player choice
            choice = get_player_choice(current_event, game_state)

            # Process the choice and update game state
            game_state = process_turn(game_state, choice)

            # Check for game over conditions
            game_state = check_game_over(game_state)

        # If no current event, advance to next one
        else:
            game_state = process_turn(game_state, None)

        # Allow saving at any time
        # In the new UI, we might want a better way to handle this, 
        # but for now we'll stick to the prompt or maybe add a menu option in the future.
        # Since we are using Rich prompts, we can't easily interrupt the flow for a save command 
        # unless we add it to the choices or handle it separately.
        # For now, let's assume autosave or save at end of turn? 
        # The original code asked for save after every turn.
        
        # Let's make it a bit smoother. We'll ask to continue or save.
        # But wait, the original code had: input("\nType 'save' to save game, or press Enter to continue: ")
        # We can replicate this with a prompt.
        
        from rich.prompt import Prompt
        action = Prompt.ask(
            "\n[dim]Press Enter to continue, type 'map' to view map, or 'save' to save[/dim]", 
            default=""
        ).lower()
        
        if action == "save":
            save_game(game_state)
            show_success_message("Game saved!")
            Prompt.ask("[dim]Press Enter to continue...[/dim]")
        elif action == "map":
            show_map(game_state)
            Prompt.ask("[dim]Press Enter to continue...[/dim]")

    # Game over screen
    show_game_over(game_state)


@app.command()
def play():
    """Start a new campaign."""
    game_state = get_initial_game_state()
    game_state = initialize_game(game_state)
    run_game_loop(game_state)


@app.command()
def load():
    """Load a saved game."""
    game_state = load_game()
    if game_state:
        run_game_loop(game_state)
    else:
        show_error_message("No saved game found.")


@app.command()
def rules():
    """View instructions."""
    show_instructions()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Napoleon's Campaign - Lead France to glory!
    """
    if ctx.invoked_subcommand is None:
        # Interactive Menu Mode
        clear_screen()
        while True:
            choice = show_main_menu()

            if choice == 1:  # Start New Campaign
                play()
            elif choice == 2:  # Load Saved Game
                load()
            elif choice == 3:  # View Instructions
                rules()
            elif choice == 4:  # Exit
                print("Thank you for playing Napoleon's Campaign!")
                raise typer.Exit()
            
            # Pause before showing menu again if we returned from a game/rules
            # But play/load/rules usually run until done or loop themselves?
            # run_game_loop runs until game over.
            # rules shows instructions and waits for enter.
            # So we just loop back to menu.
            clear_screen()


if __name__ == "__main__":
    app()
