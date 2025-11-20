"""
Napoleon's Campaign - UI Module

Handles all user interface and display logic using Rich.
"""

import os
from typing import Dict, List, Any, Tuple
from rich.console import Console
from data import get_trait, get_general, get_artifact, MAP_DIMENSIONS, TERRITORY_NODES, MAP_CONNECTIONS
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich import box

# Initialize global console
console = Console()

# Nerd Font Icons
ICON_TROOPS = ""
ICON_GOLD = ""
ICON_MORALE = ""
ICON_TERRITORY = ""
ICON_ALLY = ""
ICON_ENEMY = ""
ICON_VICTORY = ""
ICON_DEFEAT = ""
ICON_START = ""
ICON_LOAD = ""
ICON_RULES = ""
ICON_EXIT = ""
ICON_GENERAL = ""
ICON_ARTIFACT = ""


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
    menu_table.add_row(f"[bold cyan]1.[/bold cyan] {ICON_START} Start New Campaign")
    menu_table.add_row(f"[bold cyan]2.[/bold cyan] {ICON_LOAD} Load Saved Game")
    menu_table.add_row(f"[bold cyan]3.[/bold cyan] {ICON_RULES} View Instructions")
    menu_table.add_row(f"[bold cyan]4.[/bold cyan] {ICON_EXIT} Exit Game")
    
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
        f"{ICON_TROOPS} Troops: {player['troops']:,}\n"
        f"{ICON_GOLD} Gold:   {player['gold']:,}\n"
        f"{ICON_MORALE} Morale: {player['morale']}/100"
    )
    
    diplomacy = (
        f"{ICON_TERRITORY} Territories: {len(player['territories'])}\n"
        f"{ICON_ALLY} Allies:      {len(player['allies'])}\n"
        f"{ICON_ENEMY} Enemies:     {len(player['enemies'])}"
    )
    
    table.add_row(player['name'], resources, diplomacy)
    
    console.print(table)

    # Show Traits
    if player.get("traits"):
        traits_text = Text()
        for trait_id in player["traits"]:
            trait = get_trait(trait_id)
            traits_text.append(f"• {trait['name']}: ", style="bold yellow")
            traits_text.append(f"{trait['description']}\n")
        
        console.print(Panel(traits_text, title="Active Traits", border_style="yellow"))

    # Show Generals
    if player.get("generals"):
        generals_text = Text()
        for general_id in player["generals"]:
            general = get_general(general_id)
            status_color = "green" if general["status"] == "active" else "red"
            generals_text.append(f"{ICON_GENERAL} {general['name']} ({general['status'].title()}): ", style=f"bold {status_color}")
            generals_text.append(f"{general['description']}\n")
        
        console.print(Panel(generals_text, title="Generals", border_style="blue"))

    # Show Artifacts
    if player.get("artifacts"):
        artifacts_text = Text()
        for artifact_id in player["artifacts"]:
            artifact = get_artifact(artifact_id)
            artifacts_text.append(f"{ICON_ARTIFACT} {artifact['name']}: ", style="bold magenta")
            artifacts_text.append(f"{artifact['description']}\n")
        
        console.print(Panel(artifacts_text, title="Artifacts", border_style="magenta"))


class MapCanvas:
    """A simple character-based canvas for drawing the map."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[" " for _ in range(width)] for _ in range(height)]
        
    def draw_line(self, x0: int, y0: int, x1: int, y1: int, char: str = "·"):
        """Draw a line using Bresenham's algorithm."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            if 0 <= x0 < self.width and 0 <= y0 < self.height:
                # Don't overwrite existing boxes or labels if possible, but for lines we might need to.
                # Let's just draw.
                if self.grid[y0][x0] == " ":
                    self.grid[y0][x0] = char
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_box(self, x: int, y: int, w: int, h: int, label: str, border_color: str = "white"):
        """Draw a box with a label."""
        # Draw top and bottom
        for i in range(w):
            if 0 <= x + i < self.width:
                if 0 <= y < self.height:
                    self.grid[y][x + i] = f"[{border_color}]─[/{border_color}]"
                if 0 <= y + h - 1 < self.height:
                    self.grid[y + h - 1][x + i] = f"[{border_color}]─[/{border_color}]"
        
        # Draw sides
        for i in range(h):
            if 0 <= y + i < self.height:
                if 0 <= x < self.width:
                    self.grid[y + i][x] = f"[{border_color}]│[/{border_color}]"
                if 0 <= x + w - 1 < self.width:
                    self.grid[y + i][x + w - 1] = f"[{border_color}]│[/{border_color}]"
                    
        # Corners
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x] = f"[{border_color}]┌[/{border_color}]"
        if 0 <= y < self.height and 0 <= x + w - 1 < self.width:
            self.grid[y][x + w - 1] = f"[{border_color}]┐[/{border_color}]"
        if 0 <= y + h - 1 < self.height and 0 <= x < self.width:
            self.grid[y + h - 1][x] = f"[{border_color}]└[/{border_color}]"
        if 0 <= y + h - 1 < self.height and 0 <= x + w - 1 < self.width:
            self.grid[y + h - 1][x + w - 1] = f"[{border_color}]┘[/{border_color}]"
            
        # Label
        label_x = x + (w - len(label)) // 2
        label_y = y + h // 2
        if 0 <= label_y < self.height:
            for i, char in enumerate(label):
                if 0 <= label_x + i < self.width:
                    self.grid[label_y][label_x + i] = f"[bold {border_color}]{char}[/bold {border_color}]"

    def render(self) -> Text:
        """Render the grid to a Text object."""
        output = Text()
        for row in self.grid:
            output.append("".join(row) + "\n")
        return output


def show_map(game_state: Dict[str, Any]) -> None:
    """Display the game map."""
    canvas = MapCanvas(MAP_DIMENSIONS[0], MAP_DIMENSIONS[1])
    player = game_state["player"]
    
    # Draw connections first
    for start_node, end_node in MAP_CONNECTIONS:
        start = TERRITORY_NODES[start_node]
        end = TERRITORY_NODES[end_node]
        
        # Calculate centers
        start_x = start["x"] + start["w"] // 2
        start_y = start["y"] + start["h"] // 2
        end_x = end["x"] + end["w"] // 2
        end_y = end["y"] + end["h"] // 2
        
        canvas.draw_line(start_x, start_y, end_x, end_y, char="·")
        
    # Draw territories
    for name, node in TERRITORY_NODES.items():
        # Determine color
        if name in player["territories"]:
            color = "blue"
        elif name in player["enemies"]:
            color = "red"
        elif name in player["allies"]:
            color = "green"
        else:
            color = "white"
            
        canvas.draw_box(node["x"], node["y"], node["w"], node["h"], node["label"], color)
        
    console.print(Panel(canvas.render(), title="Strategic Map", border_style="blue"))


def show_event(event: Dict[str, Any]) -> None:
    """Display a historical event."""
    is_random = event.get("type") == "random"
    border_style = "red" if not is_random else "magenta"
    title_prefix = "" if not is_random else "🎲 RANDOM EVENT: "
    
    title = f"[bold {border_style}]{title_prefix}{event['title'].upper()}[/bold {border_style}]"
    if "year" in event:
        title += f" ({event['year']})"
        
    description = Markdown(event['description'])
    
    console.print(Panel(description, title=title, border_style=border_style, padding=(1, 2)))

    console.print("\n[bold]Your choices:[/bold]")
    for i, choice in enumerate(event["choices"], 1):
        console.print(f"[bold cyan]{i}.[/bold cyan] {choice['text']}")
    
    console.print(f"\n[italic]Turn: {event.get('turn_count', 'N/A')}[/italic]", style="dim")


def get_player_choice(event: Dict[str, Any], game_state: Dict[str, Any]) -> int:
    """Get the player's choice for an event."""
    num_choices = len(event["choices"])
    valid_choices = [str(i) for i in range(1, num_choices + 1)]
    
    while True:
        choice = Prompt.ask(
            f"\n[bold green]Enter your choice (or 'm' for map)[/bold green]", 
            choices=valid_choices + ["m", "M"]
        ).lower()
        
        if choice == "m":
            show_map(game_state)
            continue
            
        return int(choice) - 1  # Convert to 0-based index


def show_game_over(game_state: Dict[str, Any]) -> None:
    """Display the game over screen."""
    if game_state.get("victory_condition"):
        title = f"{ICON_VICTORY} VICTORY ACHIEVED: {game_state['victory_condition'].upper()} {ICON_VICTORY}"
        style = "bold green"
        message = "Your leadership has shaped the destiny of Europe!"
    else:
        title = f"{ICON_DEFEAT} DEFEAT {ICON_DEFEAT}"
        style = "bold red"
        message = "The empire has fallen. Your legacy will be debated for centuries."

    console.print(Panel(f"[center]{message}[/center]", title=f"[{style}]{title}[/{style}]", border_style=style.split()[-1]))

    player = game_state["player"]
    stats_table = Table(title="Final Statistics", show_header=False, box=box.SIMPLE)
    stats_table.add_row(f"{ICON_TROOPS} Troops", f"{player['troops']:,}")
    stats_table.add_row(f"{ICON_GOLD} Gold", f"{player['gold']:,}")
    stats_table.add_row(f"{ICON_MORALE} Morale", f"{player['morale']}/100")
    stats_table.add_row(f"{ICON_TERRITORY} Territories", str(len(player['territories'])))
    stats_table.add_row(f"{ICON_ALLY} Allies", str(len(player['allies'])))
    stats_table.add_row(f"{ICON_ENEMY} Enemies", str(len(player['enemies'])))
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
            
            icon = ""
            if resource == "troops": icon = ICON_TROOPS
            elif resource == "gold": icon = ICON_GOLD
            elif resource == "morale": icon = ICON_MORALE
            
            text.append(f"{icon} {resource.title()}: {sign}{change:,}\n", style=color)
            
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
        console.print(f"\n[bold green]{ICON_ALLY} Allies ({len(allies)}):[/bold green]")
        for ally in allies:
            console.print(f"  ✓ {ally}")

    if enemies:
        console.print(f"\n[bold red]{ICON_ENEMY} Enemies ({len(enemies)}):[/bold red]")
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
