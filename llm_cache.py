"""
LLM Cache Module

Caches LLM-generated events to reduce API calls and improve performance.
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class LLMCache:
    """Cache for LLM-generated game content."""
    
    def __init__(self, cache_dir: str = ".llm_cache"):
        """Initialize the cache.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate a cache key from prompt and model.
        
        Args:
            prompt: The prompt text
            model: The model name
            
        Returns:
            MD5 hash of prompt + model
        """
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key.
        
        Args:
            cache_key: The cache key
            
        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, prompt: str, model: str, max_age_hours: int = 168) -> Optional[Dict[str, Any]]:
        """Get cached response if available and not expired.
        
        Args:
            prompt: The prompt text
            model: The model name
            max_age_hours: Maximum age of cache in hours (default 7 days)
            
        Returns:
            Cached response or None if not found/expired
        """
        cache_key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
            
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
                
            # Check if expired
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > timedelta(hours=max_age_hours):
                cache_path.unlink()  # Delete expired cache
                return None
                
            return cache_data['response']
            
        except (json.JSONDecodeError, KeyError, ValueError):
            # Corrupted cache file
            cache_path.unlink()
            return None
    
    def set(self, prompt: str, model: str, response: Dict[str, Any]) -> None:
        """Cache a response.
        
        Args:
            prompt: The prompt text
            model: The model name
            response: The response to cache
        """
        cache_key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(cache_key)
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt[:100],  # Store truncated prompt for debugging
            'model': model,
            'response': response
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def clear_old(self, max_age_hours: int = 168) -> int:
        """Clear cache entries older than max_age_hours.
        
        Args:
            max_age_hours: Maximum age in hours (default 7 days)
            
        Returns:
            Number of entries cleared
        """
        count = 0
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if cached_time < cutoff:
                    cache_file.unlink()
                    count += 1
                    
            except (json.JSONDecodeError, KeyError, ValueError):
                # Corrupted file, delete it
                cache_file.unlink()
                count += 1
                
        return count
    
    def clear_all(self) -> int:
        """Clear all cache entries.
        
        Returns:
            Number of entries cleared
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in files)
        
        return {
            'total_entries': len(files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir)
        }
