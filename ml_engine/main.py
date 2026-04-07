import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services.geo_weather import get_weather_sunrise_sunset
from services.location_electricity import get_electricity_rate
from vision.yolo_detector import detect_solar_area
from models.energy_profit import calculate_energy_and_profit

app = FastAPI(title="Solar Analyzer ML Engine")

# CORS for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple in-memory rate limiting dict (IP -> [timestamps])
# In a multi-worker production environment, this would be Redis.
import time
from collections import defaultdict
ip_request_history = defaultdict(list)
RATE_LIMIT_REQUESTS = 4
RATE_LIMIT_WINDOW_SEC = 60

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Only rate limit the heavy /analyze endpoint
    if request.url.path == "/analyze" and request.method == "POST":
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old history for this IP
        ip_request_history[client_ip] = [
            t for t in ip_request_history[client_ip] 
            if current_time - t < RATE_LIMIT_WINDOW_SEC
        ]
        
        # Check limit
        if len(ip_request_history[client_ip]) >= RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many analysis requests. Please wait a minute and try again."}
            )
            
        ip_request_history[client_ip].append(current_time)

    return await call_next(request)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "ML engine is up and running"}

@app.post("/analyze")
async def analyze_solar_opportunity(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    panel_length_m: float = Form(2.0),
    panel_width_m: float = Form(1.0)
):
    try:
        # Read the image
        img_bytes = await image.read()

        # Step 1: Detect available roof/field area using YOLOv8
        area_m2 = detect_solar_area(img_bytes)

        # Step 2: Fetch weather + solar radiation data from Open-Meteo
        weather_data = get_weather_sunrise_sunset(latitude, longitude)

        # Step 3: Fetch local electricity rate using GPS reverse geocoding
        electricity_info = get_electricity_rate(latitude, longitude)

        # Step 4: Calculate with all corrections + local currency
        result = calculate_energy_and_profit(
            area_m2               = area_m2,
            panel_length          = panel_length_m,
            panel_width           = panel_width_m,
            weather_data          = weather_data,
            latitude              = latitude,
            electricity_rate_local = electricity_info["rate_local_per_kwh"],
            currency_code         = electricity_info["currency_code"],
            currency_symbol       = electricity_info["currency_symbol"]
        )

        return {
            "status": "success",
            "location": {
                "latitude":  latitude,
                "longitude": longitude
            },
            "vision_analysis": {
                "detected_area_m2": area_m2
            },
            "weather":           weather_data,
            "electricity_info":  electricity_info,
            "financial_analysis": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
