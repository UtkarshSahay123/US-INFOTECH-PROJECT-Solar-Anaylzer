import requests
from datetime import datetime
from utils.cache import weather_cache

def get_weather_sunrise_sunset(lat: float, lon: float) -> dict:
    """
    Fetches real-time weather, solar radiation, sunrise, and sunset times
    from Open-Meteo for the given coordinates. Uses a 1-hour TTL cache.
    """
    # Round coordinates to 2 decimal places specifically for weather/solar
    # weather patterns don't change drastically within 1-2 km.
    cache_key = f"{round(lat, 2)},{round(lon, 2)}"
    cached_data = weather_cache.get(cache_key)
    if cached_data:
        return cached_data

    # Using Open-Meteo for free weather data (no API key required)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunrise,sunset,uv_index_max,shortwave_radiation_sum&current_weather=true&timezone=auto"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        daily = data.get("daily", {})
        
        if not daily:
            raise ValueError("No daily data available")
            
        sunrise = daily.get("sunrise", [""])[0]
        sunset = daily.get("sunset", [""])[0]
        radiation = daily.get("shortwave_radiation_sum", [0.0])[0] # MJ/m2
        
        result = {
            "temperature_celsius": current.get("temperature", 25.0),
            "windspeed_kmh": current.get("windspeed", 0.0),
            "weather_code": current.get("weathercode", 0),
            "sunrise": sunrise,
            "sunset": sunset,
            "daily_radiation_mj_m2": radiation
        }
        weather_cache.set(cache_key, result)
        return result
    except Exception as e:
        # Fallback metrics in case API fails
        return {
            "temperature_celsius": 30.0,
            "windspeed_kmh": 5.0,
            "weather_code": 0,
            "sunrise": "06:00",
            "sunset": "18:00",
            "daily_radiation_mj_m2": 20.5,
            "error": str(e)
        }
