
import json
import os
import redis
from typing import Any, Optional

# Redis manager copied from Week 8
class Cache_Manager:
    def __init__(self):
        self._client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            username=os.getenv("REDIS_USER", ""),
            password=os.getenv("REDIS_PASSWORD", ""),
            decode_responses=True            
        )
        # Default TTL 
        self._ttl = int(os.getenv("CACHE_TTL", "300"))

    
    def get(self, key: str):
        try:
            return self._client.get(key)
        except redis.RedisError as exc:
            print("Redis GET error:", exc)
            return None

    def set(self, key, value, ttl= None) :
        try:
            self._client.setex(key, ttl or self._ttl, value)
        except redis.RedisError as exc:
            print("Redis SET error:", exc)
    #
    def delete(self, *keys):
        try:
            if keys:
                self._client.delete(*keys)
        except redis.RedisError as exc:
            print("Redis DEL error:", exc)

    
    def get_json(self, key):
        raw = self.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def set_json(self, key: str, obj: Any, ttl: Optional[int] = None):
        self.set(key, json.dumps(obj), ttl)