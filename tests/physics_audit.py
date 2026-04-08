
import math

def calculate_energy_and_profit(
    area_m2: float,
    panel_length: float,
    panel_width: float,
    weather_data: dict,
    latitude: float = 20.0,
    electricity_rate_local: float = 0.12
) -> dict:
    # Re-implementing the core logic for verification
    BASE_PANEL_EFFICIENCY = 0.20
    TEMP_COEFFICIENT = 0.004
    STC_TEMP = 25.0
    NOCT_OFFSET = 25.0
    STANDARD_PANEL_WATT = 400
    USABLE_AREA_RATIO = 0.80
    PERFORMANCE_RATIO = 0.75

    panel_area = panel_length * panel_width
    usable_area = area_m2 * USABLE_AREA_RATIO
    max_panels = math.floor(usable_area / panel_area)

    if max_panels <= 0: return {"monthly_energy": 0}

    radiation_mj = weather_data.get("daily_radiation_mj_m2", 20.0)
    peak_sun_hours = radiation_mj * 0.2778

    temp = weather_data.get("temperature_celsius", 25.0)
    cell_temp = temp + NOCT_OFFSET
    delta = cell_temp - STC_TEMP
    efficiency = BASE_PANEL_EFFICIENCY * (1.0 - TEMP_COEFFICIENT * delta)
    efficiency = max(0.10, min(0.22, efficiency))

    # Tilt factor
    abs_lat = abs(latitude)
    if abs_lat < 10: tilt = 1.04
    elif abs_lat < 20: tilt = 1.08
    elif abs_lat < 30: tilt = 1.13
    elif abs_lat < 35: tilt = 1.15
    elif abs_lat < 40: tilt = 1.14
    elif abs_lat < 50: tilt = 1.11
    elif abs_lat < 60: tilt = 1.08
    else: tilt = 1.05

    # Weather factor
    weather_code = weather_data.get("weather_code", 0)
    if weather_code == 0: shading = 1.0
    elif weather_code <= 3: shading = 0.85
    elif weather_code <= 49: shading = 0.65
    elif weather_code <= 82: shading = 0.50
    else: shading = 0.20

    total_area = max_panels * panel_area
    daily_energy = total_area * efficiency * peak_sun_hours * PERFORMANCE_RATIO * tilt * shading
    return {
        "max_panels": max_panels,
        "efficiency": efficiency,
        "daily_energy": daily_energy,
        "monthly_energy": daily_energy * 30.5
    }

def run_accuracy_audit():
    print("SolarPulse Accuracy Audit - Physics Model Verification")
    print("-" * 50)
    
    scenarios = [
        {"name": "Equatorial (Singapore)", "lat": 1.35, "temp": 32, "rad": 18, "code": 0},
        {"name": "Desert (Sahara)", "lat": 25.0, "temp": 45, "rad": 28, "code": 0},
        {"name": "Arctic (Norway)", "lat": 65.0, "temp": -5, "rad": 12, "code": 0},
        {"name": "Temperate (London)", "lat": 51.5, "temp": 15, "rad": 10, "code": 61}, # Rain
    ]
    
    for s in scenarios:
        res = calculate_energy_and_profit(100, 2.0, 1.0, {"temperature_celsius": s['temp'], "daily_radiation_mj_m2": s['rad'], "weather_code": s['code']}, s['lat'])
        print(f"Scenario: {s['name']}")
        print(f"  - Efficiency: {res['efficiency']*100:.1f}%")
        print(f"  - Max Panels: {res['max_panels']}")
        print(f"  - Monthly Energy: {res['monthly_energy']:.1f} kWh")
        print("-" * 30)

if __name__ == "__main__":
    run_accuracy_audit()
