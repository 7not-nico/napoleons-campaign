"""
NPC System for Napoleon's Campaign

Manages persistent NPCs with personality, memory, and dialogue.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class NPC:
    """Represents a persistent NPC with personality and memory."""
    
    def __init__(self, npc_id: str, name: str, role: str, personality: str, 
                 initial_relationship: int = 50):
        """Initialize an NPC.
        
        Args:
            npc_id: Unique identifier
            name: Display name
            role: NPC role (Marshal, Advisor, Diplomat, etc.)
            personality: Personality description for LLM
            initial_relationship: Initial relationship score (0-100)
        """
        self.id = npc_id
        self.name = name
        self.role = role
        self.personality = personality
        self.relationship = initial_relationship
        self.conversation_history: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
        
    def add_conversation(self, player_input: str, npc_response: str, 
                        relationship_change: int = 0):
        """Record a conversation.
        
        Args:
            player_input: What the player said
            npc_response: How the NPC responded
            relationship_change: Change in relationship (-10 to +10)
        """
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'player': player_input,
            'npc': npc_response,
            'relationship_before': self.relationship
        })
        
        self.relationship = max(0, min(100, self.relationship + relationship_change))
        
    def get_recent_history(self, count: int = 3) -> List[Dict[str, Any]]:
        """Get recent conversation history.
        
        Args:
            count: Number of recent conversations
            
        Returns:
            List of recent conversations
        """
        return self.conversation_history[-count:] if self.conversation_history else []
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for saving."""
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'personality': self.personality,
            'relationship': self.relationship,
            'conversation_history': self.conversation_history,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NPC':
        """Deserialize from dict."""
        npc = cls(
            data['id'],
            data['name'],
            data['role'],
            data['personality'],
            data.get('relationship', 50)
        )
        npc.conversation_history = data.get('conversation_history', [])
        npc.metadata = data.get('metadata', {})
        return npc


# Predefined NPCs
NPCS = {
    "ney": {
        "name": "Marshal Michel Ney",
        "role": "Marshal",
        "personality": "Brave to the point of recklessness. Fiercely loyal but impulsive. "
                      "Known as 'the Bravest of the Brave'. Advocates aggressive action. "
                      "Speaks with military directness and passion.",
        "relationship": 70
    },
    "davout": {
        "name": "Marshal Louis-Nicolas Davout",
        "role": "Marshal",
        "personality": "Disciplined, methodical, and brilliant tactician. Values preparation "
                      "and planning. Can be stern but deeply loyal. Known as 'the Iron Marshal'. "
                      "Speaks with precision and strategic insight.",
        "relationship": 65
    },
    "murat": {
        "name": "Marshal Joachim Murat",
        "role": "Marshal",
        "personality": "Flashy, charismatic cavalry commander. Brave but vain. "
                      "Loves glory and recognition. Excellent at inspiring troops. "
                      "Speaks with flair and dramatic gestures.",
        "relationship": 60
    },
    "berthier": {
        "name": "Marshal Louis-Alexandre Berthier",
        "role": "Chief of Staff",
        "personality": "Organized, efficient, detail-oriented. Master of logistics and planning. "
                      "Less interested in glory than in smooth operations. "
                      "Speaks with administrative precision.",
        "relationship": 75
    },
    "talleyrand": {
        "name": "Charles-Maurice de Talleyrand",
        "role": "Diplomat",
        "personality": "Cunning, sophisticated, politically astute. Master manipulator. "
                      "Always has hidden agendas. Speaks with diplomatic elegance and subtle irony.",
        "relationship": 40
    },
    "josephine": {
        "name": "Josephine Bonaparte",
        "role": "Spouse",
        "personality": "Elegant, charming, politically savvy. Concerned about Napoleon's well-being "
                      "and the empire's stability. Can be jealous but deeply caring. "
                      "Speaks with grace and emotional intelligence.",
        "relationship": 80
    }
}


def get_npc(npc_id: str) -> Optional[Dict[str, Any]]:
    """Get NPC definition by ID.
    
    Args:
        npc_id: NPC identifier
        
    Returns:
        NPC data or None
    """
    return NPCS.get(npc_id)


def create_npc_instance(npc_id: str) -> Optional[NPC]:
    """Create an NPC instance.
    
    Args:
        npc_id: NPC identifier
        
    Returns:
        NPC instance or None
    """
    npc_data = get_npc(npc_id)
    if not npc_data:
        return None
        
    return NPC(
        npc_id,
        npc_data['name'],
        npc_data['role'],
        npc_data['personality'],
        npc_data.get('relationship', 50)
    )


def get_available_npcs(game_state: Dict[str, Any]) -> List[str]:
    """Get list of NPCs available to talk to based on game state.
    
    Args:
        game_state: Current game state
        
    Returns:
        List of available NPC IDs
    """
    available = []
    
    # Marshals are available if recruited as generals
    player_generals = game_state.get('player', {}).get('generals', [])
    for general_id in player_generals:
        if general_id in NPCS:
            available.append(general_id)
    
    # Some NPCs are always available
    always_available = ['talleyrand', 'josephine', 'berthier']
    for npc_id in always_available:
        if npc_id not in available:
            available.append(npc_id)
    
    return available
