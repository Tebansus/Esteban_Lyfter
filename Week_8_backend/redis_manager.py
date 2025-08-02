
import json
import os
import redis


## Class manager class to handle Redis cache operations
# This class will handle all Redis cache operations
# It will connect to the Redis server and provide methods to get, set, and delete cache entries
class Cache_Manager:
    # First, the constructor initializes the Redis client with the connection details
    def __init__(self):
        self._client = redis.Redis(
            host='', # Insert your own Redis server host here
            port=4444, # Insert your own Redis server port here
            decode_responses=True, 
            username="default", # Insert your own Redis server username here
            password="" # Insert your own Redis server password here
        )
        
        self._ttl = int(os.getenv("CACHE_TTL", "300"))

    # get function to retrieve a value from the cache
    def get(self, key):
        try:
            return self._client.get(key)
        except Exception as e:
            print("GET error:", e)
            return None
    # Set function to store a value in the cache with the specified key
    # It also allows setting a time-to-live (TTL) for the cache entry
    # If TTL is not provided, it defaults to the class's _ttl attribute
    def set(self, key, value, ttl=None):
        try:
            self._client.setex(key, ttl or self._ttl, value)
        except Exception as e:
            print("SET error:", e)
    # Delete function to remove one or more keys from the cache
    def delete(self, *keys):
        try:
            if keys:
                self._client.delete(*keys)
        except Exception as e:
            print("DEL error:", e)

# get json function to retrieve a JSON object from the cache, in order to return it with the API flask jsonify response
    def get_json(self, key):
        raw = self.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None
# Set json function to store a JSON object in the cache
# It serializes the object to a JSON string before storing it
    def set_json(self, key, obj, ttl=None):
        self.set(key, json.dumps(obj), ttl)