import requests
from datetime import datetime
from utils.cache import weather_cache

def get_weather_sunrise_sunset(
    lat: float, lon: float, 
    frontend_temp: float = None, frontend_wind: float = None, 
    frontend_code: int = None, frontend_sunrise: str = "", 
    frontend_sunset: str = "", frontend_radiation: float = None
) -> dict:
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

    # Bypass Open-Meteo backend check if the frontend successfully fetched and provided it
    if frontend_sunrise and frontend_sunset and frontend_temp is not None:
        result = {
            "temperature_celsius": frontend_temp,
            "windspeed_kmh": frontend_wind or 0.0,
            "weather_code": frontend_code or 0,
            "sunrise": frontend_sunrise,
            "sunset": frontend_sunset,
            "daily_radiation_mj_m2": frontend_radiation or 20.5
        }
        weather_cache.set(cache_key, result)
        return result

    # Using Open-Meteo for free weather data (no API key required)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunrise,sunset,uv_index_max,shortwave_radiation_sum&current_weather=true&timezone=auto"
    
    try:
        response = requests.get(url, timeout=5)
        
        # If open-meteo throws a 400 Bad Request, it's often due to 
        # auto-timezone failing for empty ocean coords or unmapped areas.
        if response.status_code == 400:
            url_fallback = url.replace("timezone=auto", "timezone=GMT")
            response = requests.get(url_fallback, timeout=5)
            
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
        now = datetime.utcnow().strftime("%Y-%m-%d")
        return {
            "temperature_celsius": 30.0,
            "windspeed_kmh": 5.0,
            "weather_code": 0,
            "sunrise": f"{now}T06:00",
            "sunset": f"{now}T18:00",
            "daily_radiation_mj_m2": 20.5,
            "error": str(e)
        }
