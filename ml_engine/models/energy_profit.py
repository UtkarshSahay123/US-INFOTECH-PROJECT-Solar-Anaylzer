import math

# ─────────────────────────────────────────────────────────────────────────────
# Physics & panel constants
# ─────────────────────────────────────────────────────────────────────────────
BASE_PANEL_EFFICIENCY = 0.20    # 20% — modern monocrystalline PERC panels (STC)
TEMP_COEFFICIENT      = 0.004   # -0.4%/°C above STC temperature (industry standard)
STC_TEMP              = 25.0    # °C — Standard Test Condition temperature
NOCT_OFFSET           = 25.0    # °C — Cell is ~25°C hotter than ambient (NOCT model)
STANDARD_PANEL_WATT   = 400     # W  — Modern 400W panel (was 350W previously)
USABLE_AREA_RATIO     = 0.80    # 80% of detected roof area is actually installable
PERFORMANCE_RATIO     = 0.75    # Inverter + cable + dust + mismatch losses


def get_temp_corrected_efficiency(temp_celsius: float) -> float:
    """
    Corrects panel efficiency for real operating temperature using the NOCT model.
    Cell temperature ≈ ambient + 25°C. Panels lose ~0.4% per °C above 25°C STC.
    """
    cell_temp = temp_celsius + NOCT_OFFSET
    delta = cell_temp - STC_TEMP
    corrected = BASE_PANEL_EFFICIENCY * (1.0 - TEMP_COEFFICIENT * delta)
    return round(max(0.10, min(0.22, corrected)), 4)  # clamp 10%–22%


def get_tilt_correction_factor(latitude: float) -> float:
    """
    Returns energy gain factor for panels tilted at optimal angle (≈ latitude).
    Derived from PVGIS tilt optimisation studies.
    """
    abs_lat = abs(latitude)
    if abs_lat < 10:   return 1.04
    elif abs_lat < 20: return 1.08
    elif abs_lat < 30: return 1.13
    elif abs_lat < 35: return 1.15   # optimal zone
    elif abs_lat < 40: return 1.14
    elif abs_lat < 50: return 1.11
    elif abs_lat < 60: return 1.08
    else:              return 1.05


def get_shading_factor(weather_code: int) -> float:
    """
    Estimates energy reduction from clouds/precipitation using WMO weather codes.
    """
    if weather_code == 0:         return 1.00  # Clear
    elif weather_code <= 3:       return 0.85  # Partly cloudy
    elif weather_code <= 49:      return 0.65  # Fog
    elif weather_code <= 67:      return 0.45  # Rain / drizzle
    elif weather_code <= 77:      return 0.30  # Snow
    elif weather_code <= 82:      return 0.50  # Showers
    else:                         return 0.20  # Thunderstorm


def calculate_energy_and_profit(
    area_m2: float,
    panel_length: float,
    panel_width: float,
    weather_data: dict,
    latitude: float = 20.0,
    electricity_rate_local: float = 0.12,
    currency_code: str = "USD",
    currency_symbol: str = "$",
    manual_capacity_kw: float = None
) -> dict:
    """
    Full physics + financial model for solar energy and profit estimation.
    Profit is calculated and returned in the LOCAL CURRENCY of the user's GPS location.
    If manual_capacity_kw is provided, it overrides calculation from area_m2.
    """

    # ── 1. Panel packing ──────────────────────────────────────────────────────
    panel_area   = panel_length * panel_width
    
    if manual_capacity_kw is not None and manual_capacity_kw > 0:
        system_capacity_kw = manual_capacity_kw
        max_panels = math.ceil(system_capacity_kw / (STANDARD_PANEL_WATT / 1000.0))
        usable_area = area_m2 * USABLE_AREA_RATIO # still keep track of area if needed
    else:
        usable_area  = area_m2 * USABLE_AREA_RATIO
        max_panels   = math.floor(usable_area / panel_area)
        system_capacity_kw = max_panels * (STANDARD_PANEL_WATT / 1000.0)

    zero_result = {
        "max_panels": 0, "system_capacity_kw": 0,
        "daily_energy_kwh": 0, "monthly_energy_kwh": 0,
        "daily_profit_local": 0, "monthly_profit_local": 0,
        "monthly_profit_usd": 0,  # legacy field for DB save compat
        "panel_dimensions": f"{panel_length}x{panel_width}m",
        "panel_efficiency_pct": round(BASE_PANEL_EFFICIENCY * 100, 1),
        "tilt_correction_factor": 1.0, "shading_factor": 1.0,
        "electricity_rate_local": electricity_rate_local,
        "currency_code": currency_code, "currency_symbol": currency_symbol,
    }

    if max_panels <= 0 and (manual_capacity_kw is None or manual_capacity_kw <= 0):
        return zero_result

    # ── 2. System capacity was handled above ──────────────────────────────────

    # ── 3. Solar radiation → Peak Sun Hours ───────────────────────────────────
    radiation_mj   = weather_data.get("daily_radiation_mj_m2", 20.0)
    peak_sun_hours = radiation_mj * 0.2778   # 1 MJ/m² = 0.2778 kWh/m²

    # ── 4. Temperature-corrected efficiency ───────────────────────────────────
    temp       = weather_data.get("temperature_celsius", 25.0)
    efficiency = get_temp_corrected_efficiency(temp)

    # ── 5. Tilt correction by GPS latitude ────────────────────────────────────
    tilt_factor = get_tilt_correction_factor(latitude)

    # ── 6. Shading factor from WMO weather code ───────────────────────────────
    weather_code   = weather_data.get("weather_code", 0)
    shading_factor = get_shading_factor(weather_code)

    # ── 7. Energy: E = A × eff(T) × H × PR × tilt × shading ─────────────────
    # If manual capacity, we calculate effective area based on that capacity
    # P = A * Eff_STC * 1000 => A = P / (Eff_STC * 1000)
    # total_active_area = system_capacity_kw / (BASE_PANEL_EFFICIENCY)
    
    # Actually, it's simpler to stay consistent with panels:
    total_active_area  = max_panels * panel_area
    
    daily_energy_kwh   = (
        total_active_area * efficiency * peak_sun_hours
        * PERFORMANCE_RATIO * tilt_factor * shading_factor
    )
    monthly_energy_kwh = daily_energy_kwh * 30.5

    # ── 8. Profit in LOCAL CURRENCY ───────────────────────────────────────────
    daily_profit_local   = daily_energy_kwh   * electricity_rate_local
    monthly_profit_local = monthly_energy_kwh * electricity_rate_local

    return {
        "max_panels":             max_panels,
        "panel_dimensions":       f"{panel_length}x{panel_width}m",
        "system_capacity_kw":     round(system_capacity_kw, 2),
        "daily_energy_kwh":       round(daily_energy_kwh, 2),
        "monthly_energy_kwh":     round(monthly_energy_kwh, 2),
        # ── Financial (local currency) ────────────────────────────────────────
        "daily_profit_local":     round(daily_profit_local, 2),
        "monthly_profit_local":   round(monthly_profit_local, 2),
        "monthly_profit_usd":     round(monthly_profit_local, 2),  # legacy DB field
        "electricity_rate_local": electricity_rate_local,
        "currency_code":          currency_code,
        "currency_symbol":        currency_symbol,
        # ── Diagnostic ────────────────────────────────────────────────────────
        "panel_efficiency_pct":   round(efficiency * 100, 1),
        "tilt_correction_factor": tilt_factor,
        "shading_factor":         shading_factor,
    }
