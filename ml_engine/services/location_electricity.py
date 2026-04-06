import requests

# ─────────────────────────────────────────────────────────────────────────────
# Electricity rates in LOCAL CURRENCY per kWh, with currency metadata.
# Sources: IEA (2024), GlobalPetrolPrices.com, CERC India (FY2024), EIA USA
# ─────────────────────────────────────────────────────────────────────────────
COUNTRY_RATES = {

    # ── ASIA ──────────────────────────────────────────────────────────────────
    "IN": {
        "currency_code": "INR", "currency_symbol": "₹",
        "default": 6.83,   # ₹/kWh — national average FY2024
        "states": {
            "maharashtra":       7.94,
            "delhi":             7.40,
            "uttar pradesh":     5.56,
            "karnataka":         7.30,
            "tamil nadu":        6.73,
            "gujarat":           6.14,
            "rajasthan":         6.55,
            "west bengal":       5.89,
            "telangana":         6.81,
            "andhra pradesh":    6.64,
            "kerala":            6.38,
            "punjab":            5.83,
            "haryana":           6.22,
            "madhya pradesh":    6.06,
            "bihar":             5.23,
            "odisha":            5.73,
            "assam":             5.56,
            "jharkhand":         5.48,
            "chhattisgarh":      5.40,
            "himachal pradesh":  4.98,
            "uttarakhand":       5.64,
            "goa":               6.14,
        }
    },
    "CN": {"currency_code": "CNY", "currency_symbol": "¥",  "default": 0.60},
    "JP": {"currency_code": "JPY", "currency_symbol": "¥",  "default": 31.0},
    "KR": {"currency_code": "KRW", "currency_symbol": "₩",  "default": 148.0},
    "SG": {"currency_code": "SGD", "currency_symbol": "S$", "default": 0.268},
    "TH": {"currency_code": "THB", "currency_symbol": "฿",  "default": 4.18},
    "VN": {"currency_code": "VND", "currency_symbol": "₫",  "default": 1900.0},
    "ID": {"currency_code": "IDR", "currency_symbol": "Rp", "default": 1115.0},
    "MY": {"currency_code": "MYR", "currency_symbol": "RM", "default": 0.285},
    "PH": {"currency_code": "PHP", "currency_symbol": "₱",  "default": 8.50},
    "PK": {"currency_code": "PKR", "currency_symbol": "Rs", "default": 29.78},
    "BD": {"currency_code": "BDT", "currency_symbol": "৳",  "default": 8.65},
    "LK": {"currency_code": "LKR", "currency_symbol": "Rs", "default": 40.0},
    "NP": {"currency_code": "NPR", "currency_symbol": "Rs", "default": 13.4},

    # ── MIDDLE EAST ───────────────────────────────────────────────────────────
    "SA": {"currency_code": "SAR", "currency_symbol": "﷼",  "default": 0.18},
    "AE": {"currency_code": "AED", "currency_symbol": "د.إ","default": 0.239},
    "QA": {"currency_code": "QAR", "currency_symbol": "﷼",  "default": 0.102},
    "KW": {"currency_code": "KWD", "currency_symbol": "د.ك","default": 0.0052},
    "IR": {"currency_code": "IRR", "currency_symbol": "﷼",  "default": 1260.0},
    "IL": {"currency_code": "ILS", "currency_symbol": "₪",  "default": 0.549},
    "TR": {"currency_code": "TRY", "currency_symbol": "₺",  "default": 2.14},

    # ── EUROPE ────────────────────────────────────────────────────────────────
    "DE": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.310},
    "GB": {"currency_code": "GBP", "currency_symbol": "£",  "default": 0.242},
    "FR": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.176},
    "IT": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.267},
    "ES": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.234},
    "NL": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.285},
    "BE": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.296},
    "CH": {"currency_code": "CHF", "currency_symbol": "CHF","default": 0.192},
    "AT": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.225},
    "SE": {"currency_code": "SEK", "currency_symbol": "kr", "default": 1.48},
    "NO": {"currency_code": "NOK", "currency_symbol": "kr", "default": 1.08},
    "DK": {"currency_code": "DKK", "currency_symbol": "kr", "default": 2.61},
    "FI": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.155},
    "PL": {"currency_code": "PLN", "currency_symbol": "zł", "default": 0.71},
    "CZ": {"currency_code": "CZK", "currency_symbol": "Kč", "default": 4.32},
    "HU": {"currency_code": "HUF", "currency_symbol": "Ft", "default": 38.7},
    "PT": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.218},
    "GR": {"currency_code": "EUR", "currency_symbol": "€",  "default": 0.193},
    "RU": {"currency_code": "RUB", "currency_symbol": "₽",  "default": 2.90},

    # ── AMERICAS ──────────────────────────────────────────────────────────────
    "US": {
        "currency_code": "USD", "currency_symbol": "$",
        "default": 0.130,
        "states": {
            "california":  0.259,  "texas":      0.111,
            "new york":    0.197,  "florida":    0.122,
            "illinois":    0.132,  "ohio":       0.114,
            "georgia":     0.118,  "washington": 0.102,
            "arizona":     0.119,  "nevada":     0.131,
            "colorado":    0.118,  "hawaii":     0.388,
            "alaska":      0.224,
        }
    },
    "CA": {"currency_code": "CAD", "currency_symbol": "C$", "default": 0.156},
    "MX": {"currency_code": "MXN", "currency_symbol": "$",  "default": 1.42},
    "BR": {"currency_code": "BRL", "currency_symbol": "R$", "default": 0.493},
    "AR": {"currency_code": "ARS", "currency_symbol": "$",  "default": 56.4},
    "CL": {"currency_code": "CLP", "currency_symbol": "$",  "default": 154.0},

    # ── AFRICA ────────────────────────────────────────────────────────────────
    "ZA": {"currency_code": "ZAR", "currency_symbol": "R",  "default": 1.58},
    "NG": {"currency_code": "NGN", "currency_symbol": "₦",  "default": 68.0},
    "EG": {"currency_code": "EGP", "currency_symbol": "£",  "default": 0.83},
    "KE": {"currency_code": "KES", "currency_symbol": "KSh","default": 20.2},
    "MA": {"currency_code": "MAD", "currency_symbol": "د.م.","default": 1.32},

    # ── OCEANIA ───────────────────────────────────────────────────────────────
    "AU": {"currency_code": "AUD", "currency_symbol": "A$", "default": 0.436},
    "NZ": {"currency_code": "NZD", "currency_symbol": "NZ$","default": 0.356},
}

# Fallback: USD
DEFAULT_RATE    = 0.12
DEFAULT_CURRENCY = {"currency_code": "USD", "currency_symbol": "$"}


from utils.cache import geo_cache

def get_electricity_rate(lat: float, lon: float) -> dict:
    """
    Reverse-geocode GPS coordinates via Nominatim (OpenStreetMap, no API key).
    Returns local electricity rate in LOCAL CURRENCY per kWh + currency metadata.
    Uses a 24-hour TTL cache to prevent IP bans.
    """
    # Round coordinates to 2 decimal places to dramatically increase cache hits.
    # 2 decimal places provides ~1.1km accuracy, which is more than enough for electricity rates.
    cache_key = f"{round(lat, 2)},{round(lon, 2)}"
    cached_data = geo_cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        headers = {"User-Agent": "SolarPulse-Analyzer/1.0"}
        url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lon}&format=json&addressdetails=1"
        )
        resp = requests.get(url, headers=headers, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        address      = data.get("address", {})
        country_code = address.get("country_code", "").upper()
        country_name = address.get("country", "Unknown")
        state        = (
            address.get("state") or address.get("province") or
            address.get("region") or ""
        ).lower()

        rate_info = COUNTRY_RATES.get(country_code, {})
        rate      = rate_info.get("default", DEFAULT_RATE)
        currency_code   = rate_info.get("currency_code",   DEFAULT_CURRENCY["currency_code"])
        currency_symbol = rate_info.get("currency_symbol", DEFAULT_CURRENCY["currency_symbol"])

        # Try state-specific rate
        for state_key, state_rate in rate_info.get("states", {}).items():
            if state_key in state:
                rate = state_rate
                break

        result = {
            "rate_local_per_kwh": rate,
            "currency_code":      currency_code,
            "currency_symbol":    currency_symbol,
            "country_code":       country_code,
            "country_name":       country_name,
            "state":              address.get("state", address.get("province", "")),
            "city":               address.get("city", address.get("town", address.get("village", ""))),
            "source":             "gps_geocoded"
        }
        
        geo_cache.set(cache_key, result)
        return result

    except Exception as e:
        return {
            "rate_local_per_kwh": DEFAULT_RATE,
            "currency_code":      "USD",
            "currency_symbol":    "$",
            "country_code":       "XX",
            "country_name":       "Unknown",
            "state":              "",
            "city":               "",
            "source":             "fallback",
            "error":              str(e)
        }
