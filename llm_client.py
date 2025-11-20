"""
LLM Client for Napoleon's Campaign

Generates dynamic game text using the opencode CLI.
"""

import subprocess
import json
from typing import Dict, List, Any, Optional
from llm_cache import LLMCache


class LLMClient:
    """Client for generating game text using opencode."""
    
    def __init__(self, model: str = "google/gemini-2.0-flash", fallback_models: List[str] = None):
        """Initialize the LLM client.
        
        Uses Google's Gemini model via opencode.
        Default is google/gemini-2.0-flash (fast and capable).
        
        Args:
            model: Model to use in provider/model format
            fallback_models: List of fallback models to try if primary fails
        """
        self.model = model
        self.fallback_models = fallback_models or [
            "google/gemini-2.5-flash",
            "google/gemini-flash-latest"
        ]
        self.cache = LLMCache()
        
    def _call_opencode(self, prompt: str, use_cache: bool = True) -> str:
        """Call opencode CLI with a prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            use_cache: Whether to use caching (default True)
            
        Returns:
            The LLM's response
        """
        # Check cache first
        if use_cache:
            cached = self.cache.get(prompt, self.model)
            if cached:
                return json.dumps(cached)  # Return as JSON string
        
        # Try primary model
        models_to_try = [self.model] + self.fallback_models
        last_error = None
        
        for model in models_to_try:
            try:
                # Use opencode run for non-interactive mode
                result = subprocess.run(
                    ["opencode", "run", prompt, "--model", model],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    last_error = f"Model {model} error: {result.stderr}"
                    continue  # Try next model
                    
                response = result.stdout.strip()
                
                # Cache successful response
                if use_cache and response:
                    try:
                        # Try to parse as JSON to validate before caching
                        parsed = json.loads(response) if response.startswith('{') else response
                        self.cache.set(prompt, model, parsed if isinstance(parsed, dict) else {"text": response})
                    except json.JSONDecodeError:
                        pass  # Don't cache malformed responses
                
                return response
                
            except subprocess.TimeoutExpired:
                last_error = f"Model {model} timed out"
                continue
            except FileNotFoundError:
                raise Exception("opencode not found. Please install it.")
        
        # All models failed
        raise Exception(f"All models failed. Last error: {last_error}")
    
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
            
        # Add active goals to context
        from goals_system import get_active_goals
        active_goals = get_active_goals(game_state)
        if active_goals:
            context += "\nACTIVE PLAYER GOALS:\n"
            for goal in active_goals:
                context += f"- {goal.description} (Progress: {goal.progress}%)\n"
            
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
    
    def generate_npc_dialogue(self, npc: Any, game_state: Dict[str, Any], 
                             player_input: str) -> Dict[str, Any]:
        """Generate NPC dialogue response.
        
        Args:
            npc: NPC instance with personality and history
            game_state: Current game state
            player_input: What the player said/asked
            
        Returns:
            Dict with 'response' and 'relationship_change'
        """
        player = game_state["player"]
        
        # Build context
        context = f"""You are {npc.name}, a character in Napoleon's Campaign.

YOUR ROLE: {npc.role}
YOUR PERSONALITY: {npc.personality}

CURRENT RELATIONSHIP WITH NAPOLEON: {npc.relationship}/100
({"Very loyal" if npc.relationship > 70 else "Loyal" if npc.relationship > 50 else "Neutral" if npc.relationship > 30 else "Distrustful"})

GAME STATE:
- Year: {game_state['year']}
- Season: {game_state['season']}
- Napoleon's Troops: {player['troops']:,}
- Napoleon's Gold: {player['gold']:,}
- Napoleon's Morale: {player['morale']}/100
- Territories: {', '.join(player['territories'])}
- Allies: {', '.join(player['allies']) if player['allies'] else 'None'}
- Enemies: {', '.join(player['enemies'])}
"""
        
        # Add recent conversation history
        recent = npc.get_recent_history(3)
        if recent:
            context += "\nRECENT CONVERSATION HISTORY:\n"
            for conv in recent:
                context += f"Napoleon: {conv['player']}\n"
                context += f"You: {conv['npc']}\n"
        
        prompt = context + f"""\n
NAPOLEON SAYS: "{player_input}"

Respond in character. Your response should:
1. Reflect your personality and current relationship
2. Reference the game state if relevant
3. Be 1-3 sentences (concise but in-character)
4. Use appropriate tone and period-appropriate language

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "response": "Your response here",
  "relationship_change": 0
}}

relationship_change should be -5 to +5 based on:
- Positive: Napoleon's request aligns with your personality/values
- Negative: Napoleon's request conflicts with your personality/values
- Zero: Neutral interaction

Return ONLY the JSON, nothing else."""
        
        response = self._call_opencode(prompt, use_cache=False)  # Don't cache dialogue
        
        try:
            # Remove markdown if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
                
            dialogue_data = json.loads(response)
            
            # Validate and sanitize
            if 'response' not in dialogue_data:
                dialogue_data['response'] = "My apologies, I seem to have lost my train of thought."
            if 'relationship_change' not in dialogue_data:
                dialogue_data['relationship_change'] = 0
            
            # Clamp relationship change
            dialogue_data['relationship_change'] = max(-5, min(5, dialogue_data['relationship_change']))
            
            return dialogue_data
            
        except json.JSONDecodeError:
            # Fallback
            return {
                "response": "Forgive me, mon Empereur, I am deep in thought at the moment.",
                "relationship_change": 0
            }
