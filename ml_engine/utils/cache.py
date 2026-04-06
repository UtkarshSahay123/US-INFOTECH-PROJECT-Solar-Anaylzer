import time
from threading import Lock

class TTLCache:
    """
    A simple thread-safe in-memory cache with Time-To-Live (TTL).
    Used to prevent rate-limit bans from external APIs (Nominatim, Open-Meteo) in production.
    """
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
        self.cache = {}
        self.lock = Lock()

    def get(self, key: str):
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if time.time() - entry['timestamp'] < self.ttl:
                    return entry['data']
                else:
                    del self.cache[key]
        return None

    def set(self, key: str, value: any):
        with self.lock:
            self.cache[key] = {
                'data': value,
                'timestamp': time.time()
            }

    def clear(self):
        with self.lock:
            self.cache.clear()

# Global cache instances
# Reverse Geocoding is highly static. Cache for 24 hours (86400s) to strictly respect Nominatim.
geo_cache = TTLCache(ttl_seconds=86400)

# Weather data fluctuates, so cache for 1 hour (3600s).
weather_cache = TTLCache(ttl_seconds=3600)
