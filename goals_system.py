"""
Goals System for Napoleon's Campaign

Allows players to set custom objectives and tracks progress.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class GoalStatus(Enum):
    """Status of a goal."""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class GoalType(Enum):
    """Type of goal."""
    CONQUEST = "conquest"  # Territory control
    DIPLOMATIC = "diplomatic"  # Alliances, treaties
    ECONOMIC = "economic"  # Gold, resources
    MILITARY = "military"  # Army strength
    TEMPORAL = "temporal"  # Time-based
    CUSTOM = "custom"  # Free-form


class Goal:
    """Represents a player-defined goal."""
    
    def __init__(self, goal_id: str, description: str, goal_type: GoalType = GoalType.CUSTOM):
        """Initialize a goal.
        
        Args:
            goal_id: Unique identifier
            description: Player's goal description
            goal_type: Type of goal (auto-detected or custom)
        """
        self.id = goal_id
        self.description = description
        self.type = goal_type
        self.status = GoalStatus.ACTIVE
        self.created_at = datetime.now().isoformat()
        self.progress = 0  # 0-100
        self.target_conditions: Dict[str, Any] = {}
        self.events_generated = 0
        self.notes: List[str] = []
        
    def add_note(self, note: str):
        """Add a progress note."""
        self.notes.append({
            'timestamp': datetime.now().isoformat(),
            'text': note
        })
        
    def update_progress(self, new_progress: int):
        """Update progress (0-100)."""
        self.progress = max(0, min(100, new_progress))
        
        if self.progress >= 100:
            self.status = GoalStatus.COMPLETED
            
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict."""
        return {
            'id': self.id,
            'description': self.description,
            'type': self.type.value,
            'status': self.status.value,
            'created_at': self.created_at,
            'progress': self.progress,
            'target_conditions': self.target_conditions,
            'events_generated': self.events_generated,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Goal':
        """Deserialize from dict."""
        goal = cls(
            data['id'],
            data['description'],
            GoalType(data['type'])
        )
        goal.status = GoalStatus(data['status'])
        goal.created_at = data.get('created_at', datetime.now().isoformat())
        goal.progress = data.get('progress', 0)
        goal.target_conditions = data.get('target_conditions', {})
        goal.events_generated = data.get('events_generated', 0)
        goal.notes = data.get('notes', [])
        return goal


def parse_goal(description: str) -> Dict[str, Any]:
    """Parse a goal description to extract type and targets.
    
    Args:
        description: Player's goal description
        
    Returns:
        Dict with parsed goal info (type, keywords, estimated_difficulty)
    """
    desc_lower = description.lower()
    
    # Detect goal type
    goal_type = GoalType.CUSTOM
    keywords = []
    difficulty = 5  # 1-10 scale
    
    # Conquest goals
    if any(word in desc_lower for word in ['conquer', 'control', 'capture', 'take', 'territory']):
        goal_type = GoalType.CONQUEST
        keywords.extend(['military', 'expansion', 'territory'])
        difficulty = 7
        
    # Diplomatic goals
    elif any(word in desc_lower for word in ['ally', 'alliance', 'peace', 'treaty', 'negotiate']):
        goal_type = GoalType.DIPLOMATIC
        keywords.extend(['diplomacy', 'relations', 'peace'])
        difficulty = 6
        
    # Economic goals
    elif any(word in desc_lower for word in ['gold', 'wealth', 'trade', 'economy', 'rich']):
        goal_type = GoalType.ECONOMIC
        keywords.extend(['economy', 'trade', 'resources'])
        difficulty = 5
        
    # Military goals
    elif any(word in desc_lower for word in ['army', 'troops', 'soldiers', 'military', 'force']):
        goal_type = GoalType.MILITARY
        keywords.extend(['military', 'army', 'strength'])
        difficulty = 6
        
    # Temporal goals
    elif any(word in desc_lower for word in ['by', 'before', 'until', 'within']):
        goal_type = GoalType.TEMPORAL
        keywords.extend(['time-sensitive', 'deadline'])
        difficulty = 8
    
    # Extract mentioned territories
    common_territories = ['italy', 'spain', 'britain', 'russia', 'austria', 'prussia', 'germany']
    mentioned_territories = [t for t in common_territories if t in desc_lower]
    
    return {
        'type': goal_type,
        'keywords': keywords,
        'territories': mentioned_territories,
        'difficulty': difficulty
    }


def check_goal_progress(goal: Goal, game_state: Dict[str, Any]) -> int:
    """Check goal progress based on game state.
    
    Args:
        goal: The goal to check
        game_state: Current game state
        
    Returns:
        Progress percentage (0-100)
    """
    player = game_state.get('player', {})
    
    # Parse goal for targets
    parsed = parse_goal(goal.description)
    
    # Conquest goals - check territory control
    if goal.type == GoalType.CONQUEST and parsed['territories']:
        controlled = sum(1 for t in parsed['territories'] 
                        if t.capitalize() in player.get('territories', []))
        progress = int((controlled / len(parsed['territories'])) * 100)
        return progress
        
    # Economic goals - estimate based on gold
    elif goal.type == GoalType.ECONOMIC:
        current_gold = player.get('gold', 0)
        # Assume goal is to have 50k+ gold
        progress = min(100, int((current_gold / 50000) * 100))
        return progress
        
    # Military goals - based on troop strength
    elif goal.type == GoalType.MILITARY:
        current_troops = player.get('troops', 0)
        # Assume goal is 100k+ troops
        progress = min(100, int((current_troops / 100000) * 100))
        return progress
        
    # For other goals, return current progress (manually updated)
    return goal.progress


def get_active_goals(game_state: Dict[str, Any]) -> List[Goal]:
    """Get all active goals.
    
    Args:
        game_state: Current game state
        
    Returns:
        List of active Goal instances
    """
    goals_data = game_state.get('goals', [])
    goals = [Goal.from_dict(g) for g in goals_data]
    return [g for g in goals if g.status == GoalStatus.ACTIVE]
