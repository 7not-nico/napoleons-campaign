"""
LLM Client for Napoleon's Campaign

Generates dynamic game text using the opencode CLI.
"""

import subprocess
import json
from typing import Dict, List, Any, Optional


class LLMClient:
    """Client for generating game text using opencode."""
    
    def __init__(self, model: str = "google/gemini-2.0-flash"):
        """Initialize the LLM client.
        
        Uses Google's Gemini model via opencode.
        Default is google/gemini-2.0-flash (fast and capable).
        
        Args:
            model: Model to use in provider/model format
        """
        self.model = model
        
    def _call_opencode(self, prompt: str) -> str:
        """Call opencode CLI with a prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            The LLM's response
        """
        try:
            # Use opencode run for non-interactive mode
            result = subprocess.run(
                ["opencode", "run", prompt, "--model", self.model],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                raise Exception(f"opencode error: {result.stderr}")
                
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise Exception("LLM request timed out")
        except FileNotFoundError:
            raise Exception("opencode not found. Please install it.")
    
    def generate_event(self, game_state: Dict[str, Any], event_trigger: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a dynamic event based on game state.
        
        Args:
            game_state: Current game state
            event_trigger: Metadata about the event (year, type, historical context)
            
        Returns:
            Generated event with title, description, and choices
        """
        player = game_state["player"]
        
        # Build context
        context = f"""You are narrating Napoleon's Campaign, a historical strategy game.

CURRENT GAME STATE:
- Year: {game_state['year']}
- Season: {game_state['season']}
- Troops: {player['troops']:,}
- Gold: {player['gold']:,}
- Morale: {player['morale']}/100
- Territories: {', '.join(player['territories'])}
- Allies: {', '.join(player['allies']) if player['allies'] else 'None'}
- Enemies: {', '.join(player['enemies'])}
"""
        
        if player.get('traits'):
            context += f"- Napoleon's Traits: {', '.join(player['traits'])}\n"
        if player.get('generals'):
            context += f"- Active Generals: {', '.join(player['generals'])}\n"
        if player.get('artifacts'):
            context += f"- Artifacts: {', '.join(player['artifacts'])}\n"
            
        # Event type specific prompts
        if event_trigger.get('type') == 'random':
            event_prompt = f"""Generate a RANDOM EVENT for Napoleon during {game_state['year']}.
This should be a non-historical situation that arises from campaign conditions.
Examples: supply issues, political intrigue, opportunity to recruit a general, discovery of an artifact."""
        else:
            event_prompt = f"""Generate a HISTORICAL EVENT for the year {game_state['year']}.
Historical Context: {event_trigger.get('historical_context', 'Major military campaign')}
The event should be based on real Napoleonic history but adapted to current game state."""
        
        prompt = context + "\n" + event_prompt + """

Return ONLY valid JSON in this exact format (no markdown, no code blocks):
{
  "title": "Event Title (10 words max)",
  "description": "Engaging narrative description (50-100 words)",
  "choices": [
    {
      "text": "Choice 1 description",
      "consequences": {"troops": 0, "gold": 0, "morale": 0}
    },
    {
      "text": "Choice 2 description",
      "consequences": {"troops": 0, "gold": 0, "morale": 0}
    }
  ]
}

IMPORTANT RULES:
- Exactly 2-4 choices
- Consequences must be balanced (not too extreme)
- Use Napoleonic-era language and tone
- Keep descriptions concise but vivid
- Return ONLY the JSON, nothing else"""
        
        response = self._call_opencode(prompt)
        
        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
                
            event_data = json.loads(response)
            
            # Add metadata
            event_data["id"] = event_trigger.get("id", "llm_generated")
            event_data["type"] = event_trigger.get("type", "historical")
            if "year" in event_trigger:
                event_data["year"] = event_trigger["year"]
                
            return event_data
        except json.JSONDecodeError as e:
            # Fallback to a safe error event
            return {
                "id": "error",
                "title": "Unexpected Development",
                "description": f"Intelligence reports are unclear. (LLM Error: {str(e)})",
                "type": event_trigger.get("type", "random"),
                "choices": [
                    {
                        "text": "Proceed cautiously",
                        "consequences": {}
                    }
                ]
            }
