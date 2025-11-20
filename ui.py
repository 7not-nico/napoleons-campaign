"""
Napoleon's Campaign - UI Module

Handles all user interface and display logic using Rich.
"""

import os
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import IntPrompt, Confirm
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich import box

# Initialize global console
console = Console()


def clear_screen() -> None:
    """Clear the terminal screen."""
    console.clear()


def show_main_menu() -> int:
    """Display the main menu and get user choice."""
    console.print(
        Panel.fit(
            "[bold gold1]NAPOLEON'S CAMPAIGN[/bold gold1]\n[italic]A Historical Strategy Game[/italic]",
            border_style="blue",
            padding=(1, 2),
        )
    )
    
    menu_table = Table(show_header=False, box=None)
    menu_table.add_row("[bold cyan]1.[/bold cyan] Start New Campaign")
    menu_table.add_row("[bold cyan]2.[/bold cyan] Load Saved Game")
    menu_table.add_row("[bold cyan]3.[/bold cyan] View Instructions")
    menu_table.add_row("[bold cyan]4.[/bold cyan] Exit Game")
    
    console.print(menu_table)
    
    return IntPrompt.ask("\n[bold green]Enter your choice[/bold green]", choices=["1", "2", "3", "4"])


def show_status(game_state: Dict[str, Any]) -> None:
    """Display the current game status."""
    player = game_state["player"]
    
    # Create a main table for status
    table = Table(title=f"Year: {game_state['year']} | Season: {game_state['season'].title()}", box=box.ROUNDED, expand=True)
    
    table.add_column("Emperor", style="bold gold1")
    table.add_column("Resources", style="cyan")
    table.add_column("Diplomacy", style="magenta")
    
    resources = (
        f"Troops: {player['troops']:,}\n"
        f"Gold:   {player['gold']:,}\n"
        f"Morale: {player['morale']}/100"
    )
    
    diplomacy = (
        f"Territories: {len(player['territories'])}\n"
        f"Allies:      {len(player['allies'])}\n"
        f"Enemies:     {len(player['enemies'])}"
    )
    
    table.add_row(player['name'], resources, diplomacy)
    
    console.print(table)


def show_event(event: Dict[str, Any]) -> None:
    """Display a historical event."""
    title = f"[bold red]{event['title'].upper()}[/bold red] ({event['year']})"
    description = Markdown(event['description'])
    
    console.print(Panel(description, title=title, border_style="red", padding=(1, 2)))

    console.print("\n[bold]Your choices:[/bold]")
    for i, choice in enumerate(event["choices"], 1):
        console.print(f"[bold cyan]{i}.[/bold cyan] {choice['text']}")
    
    console.print(f"\n[italic]Turn: {event.get('turn_count', 'N/A')}[/italic]", style="dim")


def get_player_choice(event: Dict[str, Any]) -> int:
    """Get the player's choice for an event."""
    num_choices = len(event["choices"])
    choices_str = [str(i) for i in range(1, num_choices + 1)]
    
    choice = IntPrompt.ask(
        f"\n[bold green]Enter your choice[/bold green]", 
        choices=choices_str
    )
    return choice - 1  # Convert to 0-based index


def show_game_over(game_state: Dict[str, Any]) -> None:
    """Display the game over screen."""
    if game_state.get("victory_condition"):
        title = f"🎉 VICTORY ACHIEVED: {game_state['victory_condition'].upper()} 🎉"
        style = "bold green"
        message = "Your leadership has shaped the destiny of Europe!"
    else:
        title = "💔 DEFEAT 💔"
        style = "bold red"
        message = "The empire has fallen. Your legacy will be debated for centuries."

    console.print(Panel(f"[center]{message}[/center]", title=f"[{style}]{title}[/{style}]", border_style=style.split()[-1]))

    player = game_state["player"]
    stats_table = Table(title="Final Statistics", show_header=False, box=box.SIMPLE)
    stats_table.add_row("Troops", f"{player['troops']:,}")
    stats_table.add_row("Gold", f"{player['gold']:,}")
    stats_table.add_row("Morale", f"{player['morale']}/100")
    stats_table.add_row("Territories", str(len(player['territories'])))
    stats_table.add_row("Allies", str(len(player['allies'])))
    stats_table.add_row("Enemies", str(len(player['enemies'])))
    stats_table.add_row("Years in Power", str(game_state['year'] - 1796))
    stats_table.add_row("Historical Accuracy", f"{game_state['historical_accuracy']}%")
    
    console.print(stats_table)


def show_instructions() -> None:
    """Display detailed game instructions."""
    clear_screen()
    
    markdown_text = """
# NAPOLEON'S CAMPAIGN - INSTRUCTIONS

## OVERVIEW
You are **Napoleon Bonaparte**, commanding France through the turbulent years of the French Revolution and Napoleonic Wars.

## GAMEPLAY
- Make strategic decisions at key historical moments
- Manage your troops, gold, morale, and territories
- Fight battles and form diplomatic alliances
- Your choices determine the fate of Europe

## RESOURCES
- **TROOPS**: Military strength for battles
- **GOLD**: Economic power and army maintenance
- **MORALE**: Public support and army effectiveness
- **TERRITORIES**: Land control and resource generation

## VICTORY CONDITIONS
- **Military**: Control most of Europe
- **Diplomatic**: Form lasting alliances
- **Historical**: Follow Napoleon's actual path

## DEFEAT CONDITIONS
- Troops below 5,000
- Gold below 0
- Morale below 20
- Lose France

## CONTROLS
- Use number keys to select options
- Type 'save' to save your progress
- Follow on-screen prompts
    """
    
    console.print(Markdown(markdown_text))
    console.input("\n[dim]Press Enter to continue...[/dim]")


def show_battle_result(
    attacker: str, defender: str, result: str, casualties: int
) -> None:
    """Display battle results."""
    color = "green" if result == "victory" else "red"
    
    panel = Panel(
        f"[bold]{attacker} vs {defender}[/bold]\n"
        f"Outcome: [{color}]{result.upper()}[/{color}]\n"
        f"Casualties: {casualties:,}",
        title="BATTLE RESULT",
        border_style=color
    )
    console.print(panel)


def show_diplomacy_result(nation: str, result: str, gold_change: int = 0) -> None:
    """Display diplomacy results."""
    content = f"Nation: [bold]{nation}[/bold]\nResult: {result}"
    if gold_change != 0:
        sign = "+" if gold_change > 0 else ""
        color = "green" if gold_change > 0 else "red"
        content += f"\nGold Change: [{color}]{sign}{gold_change:,}[/{color}]"
        
    console.print(Panel(content, title="DIPLOMACY RESULT", border_style="magenta"))


def show_resource_change(changes: Dict[str, int]) -> None:
    """Display resource changes after an event."""
    if not changes:
        return
        
    text = Text()
    for resource, change in changes.items():
        if change != 0:
            sign = "+" if change > 0 else ""
            color = "green" if change > 0 else "red"
            text.append(f"{resource.title()}: {sign}{change:,}\n", style=color)
            
    console.print(Panel(text, title="Resource Changes", border_style="blue", width=40))


def show_territories(territories: List[str]) -> None:
    """Display controlled territories."""
    if territories:
        console.print(f"\n[bold]Controlled Territories ({len(territories)}):[/bold]")
        for territory in territories:
            console.print(f"  • {territory}")
    else:
        console.print("\n[dim]No territories controlled.[/dim]")


def show_allies_and_enemies(allies: List[str], enemies: List[str]) -> None:
    """Display current diplomatic status."""
    if allies:
        console.print(f"\n[bold green]Allies ({len(allies)}):[/bold green]")
        for ally in allies:
            console.print(f"  ✓ {ally}")

    if enemies:
        console.print(f"\n[bold red]Enemies ({len(enemies)}):[/bold red]")
        for enemy in enemies:
            console.print(f"  ✗ {enemy}")


def show_historical_note(event_id: str) -> None:
    """Display educational historical notes."""
    notes = {
        "italian_campaign_1796": "Napoleon's first major victory established his reputation as a military genius.",
        "austerlitz_campaign_1805": "Considered Napoleon's masterpiece, this battle destroyed the Third Coalition.",
        "russian_campaign_1812": "The disastrous invasion led to the collapse of the Grande Armée.",
        "waterloo_1815": "The final defeat ended Napoleon's Hundred Days and his imperial ambitions.",
    }

    if event_id in notes:
        console.print(Panel(f"[italic]{notes[event_id]}[/italic]", title="📚 Historical Note", border_style="yellow"))


def show_loading_message(message: str = "Loading...") -> None:
    """Display a loading message."""
    console.print(f"[dim]{message}[/dim]")


def show_error_message(message: str) -> None:
    """Display an error message."""
    console.print(f"[bold red]❌ Error: {message}[/bold red]")


def show_success_message(message: str) -> None:
    """Display a success message."""
    console.print(f"[bold green]✅ {message}[/bold green]")


def confirm_action(message: str) -> bool:
    """Get user confirmation for an action."""
    return Confirm.ask(message)
