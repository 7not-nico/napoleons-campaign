"""
Goal Management Handler
"""

from goals_system import Goal, GoalType, parse_goal, get_active_goals, check_goal_progress, GoalStatus
from ui import console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
import uuid


def show_goals(game_state):
    """Display all active goals."""
    from goals_system import get_active_goals
    
    active_goals = get_active_goals(game_state)
    
    if not active_goals:
        console.print("[dim]You have no active goals.[/dim]\\n")
        return
    
    console.print(Panel.fit(
        "[bold cyan]🎯 Your Objectives[/bold cyan]",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Goal", style="white")
    table.add_column("Progress", justify="center", style="yellow")
    table.add_column("Type", justify="center", style="dim")
    
    for goal in active_goals:
        # Update progress
        new_progress = check_goal_progress(goal, game_state)
        if new_progress != goal.progress:
            goal.update_progress(new_progress)
            # Save updated goal
            for i, g in enumerate(game_state.get('goals', [])):
                if g['id'] == goal.id:
                    game_state['goals'][i] = goal.to_dict()
                    break
        
        progress_bar = "█" * (goal.progress // 10) + "░" * (10 - goal.progress // 10)
        progress_text = f"{progress_bar} {goal.progress}%"
        
        table.add_row(
            goal.description,
            progress_text,
            goal.type.value
        )
    
    console.print(table)
    console.print()


def add_goal(game_state):
    """Add a new goal."""
    console.print(Panel.fit(
        "[bold cyan]🎯 Set a New Objective[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print("[dim]Examples:[/dim]")
    console.print("  - Conquer Italy by 1800")
    console.print("  - Form an alliance with Spain")
    console.print("  - Amass 100,000 troops")
    console.print("  - Control all of central Europe\\n")
    
    description = Prompt.ask("[bold]Your goal[/bold]")
    
    if not description or description.lower() == "cancel":
        return
    
    # Parse goal
    parsed = parse_goal(description)
    
    # Create goal
    goal_id = str(uuid.uuid4())[:8]
    goal = Goal(goal_id, description, parsed['type'])
    
    # Add to game state
    if 'goals' not in game_state:
        game_state['goals'] = []
    game_state['goals'].append(goal.to_dict())
    
    console.print(f"\\n[green]✓ Goal added:[/green] {description}")
    console.print(f"[dim]Type: {parsed['type'].value} | Difficulty: {parsed['difficulty']}/10[/dim]\\n")


def handle_goals(game_state):
    """Handle goal management."""
    while True:
        console.print("\\n[bold cyan]Goal Management[/bold cyan]")
        console.print("1. View active goals")
        console.print("2. Add new goal")
        console.print("3. Back\\n")
        
        choice = Prompt.ask("[bold]Choose[/bold]", choices=["1", "2", "3"])
        
        if choice == "1":
            show_goals(game_state)
            Prompt.ask("[dim]Press Enter to continue...[/dim]")
        elif choice == "2":
            add_goal(game_state)
        elif choice == "3":
            break
