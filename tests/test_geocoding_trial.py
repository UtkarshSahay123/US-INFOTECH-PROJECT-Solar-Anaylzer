"""
Trial run: End-to-end test of GPS geocoding -> electricity rate detection.
Tests BigDataCloud API for Andhra Pradesh, India coordinates.
"""
import requests

COUNTRY_RATES_IN = {
    "currency_code": "INR", "currency_symbol": "Rs",
    "default": 6.83,
    "states": {
        "maharashtra": 7.94, "delhi": 7.40, "uttar pradesh": 5.56,
        "karnataka": 7.30, "tamil nadu": 6.73, "gujarat": 6.14,
        "rajasthan": 6.55, "west bengal": 5.89, "telangana": 6.81,
        "andhra pradesh": 6.64, "kerala": 6.38, "punjab": 5.83,
        "haryana": 6.22, "madhya pradesh": 6.06, "bihar": 5.23,
        "odisha": 5.73, "assam": 5.56, "jharkhand": 5.48,
        "chhattisgarh": 5.40, "himachal pradesh": 4.98, "uttarakhand": 5.64,
        "goa": 6.14,
    }
}

DEFAULT_RATE = 0.12

print("=" * 60)
print("TRIAL RUN: Andhra Pradesh GPS Geocoding")
print("=" * 60)

lat, lon = 16.5062, 80.6480

print("\n[1] Calling BigDataCloud API for (%s, %s)..." % (lat, lon))
try:
    url = "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=%s&longitude=%s&localityLanguage=en" % (lat, lon)
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    data = resp.json()

    country_code = data.get("countryCode", "").upper()
    country_name = data.get("countryName", "Unknown")
    state = data.get("principalSubdivision", "").lower()
    city = data.get("locality", "")

    print("    [OK] API Response (HTTP %s)" % resp.status_code)
    print("    Country Code : %s" % country_code)
    print("    Country Name : %s" % country_name)
    print("    State        : %s" % state)
    print("    City/Locality: %s" % city)
except Exception as e:
    print("    [FAIL] API ERROR: %s" % e)
    country_code = "XX"
    state = ""

print("\n[2] Looking up electricity rate...")

if country_code == "IN":
    rate = COUNTRY_RATES_IN["default"]
    currency_code = COUNTRY_RATES_IN["currency_code"]
    currency_symbol = COUNTRY_RATES_IN["currency_symbol"]

    matched_state = None
    for state_key, state_rate in COUNTRY_RATES_IN["states"].items():
        if state_key in state:
            rate = state_rate
            matched_state = state_key
            break

    if matched_state:
        print("    [OK] State-specific rate matched: '%s'" % matched_state)
    else:
        print("    [WARN] No state match, using national default")

    print("    Rate     : %s %s/kWh" % (currency_symbol, rate))
    print("    Currency : %s" % currency_code)
    print("    Source   : gps_geocoded")
else:
    print("    [FAIL] Country code '%s' is not 'IN'" % country_code)

print("\n[3] Verification:")
expected_rate = 6.64
if country_code == "IN" and "andhra pradesh" in state and rate == expected_rate:
    print("    [PASS] Andhra Pradesh detected, rate = Rs %s/kWh (expected Rs %s)" % (rate, expected_rate))
else:
    print("    [FAIL] Got country=%s, state='%s', rate=%s" % (country_code, state, rate))
    print("           Expected: country=IN, state='andhra pradesh', rate=%s" % expected_rate)

print("\n[4] Confirming old Nominatim API is blocked...")
try:
    nom_resp = requests.get(
        "https://nominatim.openstreetmap.org/reverse?lat=%s&lon=%s&format=json" % (lat, lon),
        headers={"User-Agent": "SolarPulse-Analyzer/1.0 (test@example.com)"},
        timeout=5
    )
    print("    Nominatim HTTP Status: %s" % nom_resp.status_code)
    if nom_resp.status_code == 403:
        print("    [CONFIRMED] Nominatim returns 403 Forbidden -- BigDataCloud switch was correct")
    else:
        print("    [INFO] Nominatim returned %s (may work locally but blocks on Render)" % nom_resp.status_code)
except Exception as e:
    print("    [INFO] Nominatim connection error: %s" % e)

print("\n" + "=" * 60)
print("TRIAL COMPLETE")
print("=" * 60)
