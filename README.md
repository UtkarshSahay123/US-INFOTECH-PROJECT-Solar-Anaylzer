# ☀️ SolarPulse (Solar Analyzer) — Production Ready 🚀

**SolarPulse** is a full-stack, AI-powered platform for assessing solar panel feasibility. By utilizing computer vision (YOLOv8) to analyze rooftop imagery, calculating highly accurate solar potential, and tracking historical analyses using a robust Spring Boot backend, SolarPulse empowers seamless green energy planning.

---

## 🏗️ Production Architecture (Cloud Deployed)

The platform is now fully hosted and available globally:

| Tier | Hosting Provider | Tech Stack | Live Status |
|------|------------------|------------|-------------|
| **1. Frontend Interface** | **Vercel** | HTML5, Tailwind CSS, Vanilla JS | [Live on Vercel](https://us-infotech-project-solar-anaylzer.vercel.app) |
| **2. Auth & Data Backend**| **Render (Docker)** | Java 17, Spring Boot, Spring Security | [Backend API](https://us-infotech-project-solar-anaylzer.onrender.com) |
| **3. ML & Vision Engine** | **Render (Python)** | Python 3, FastAPI, YOLOv8, OpenCV | [ML Engine](https://solarpulse-ml-engine.onrender.com) |
| **4. Cloud Database** | **Neon** | Serverless PostgreSQL | Connected (Production) |

---

## ✨ Features

- **Object Segmentation (AI)**: Detects absolute rooftop surface area using computer vision (`yolov8n-seg`).
- **Comprehensive Analytics**: Calculates system capacity (kW), max panels, projected energy (kWh), and financial savings.
- **Robust Authentication**: 
  - JWT Stateless sessions
  - Single Sign-On (SSO) with **Google** and **Microsoft**.
- **Self-Service Password Reset**: Secure 6-digit Email OTP mechanism with `spring-boot-starter-mail`.
- **History Tracking**: Seamlessly save and browse past dashboard calculations globally. 
- **Dynamic UX**: Animated, responsive Dark/Light themes.

---

## 🔧 Production Environment Setup

The production services are configured via **Environment Variables** on Render. Do not store these in the repository:

### Backend (Render)
- `SPRING_DATASOURCE_URL`: JDBC Pooler Link from Neon.
- `SPRING_DATASOURCE_USERNAME`: Neon DB Username.
- `SPRING_DATASOURCE_PASSWORD`: Neon DB Password.
- `JWT_SECRET`: Secure 256-bit key for session signing.
- `EMAIL_USER` / `EMAIL_PASS`: Gmail App Credentials for OTP.
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`: Google OAuth2 credentials.
- `MS_CLIENT_ID` / `MS_CLIENT_SECRET`: Microsoft Azure Portal credentials.

### ML Engine (Render)
- **Root Directory**: `ml_engine`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

---

## 🚀 Local Development Setup

If you wish to run this project locally, ensure you have Java 17, Python 3.10+, and PostgreSQL installed.

### 1. Database Setup
Create a database named `solar_analyzer_auth` in your local PostgreSQL.

### 2. Start Backend
```bash
cd stitch/authentication/authentication/demo
./mvnw spring-boot:run
```

### 3. Start ML Engine
```bash
cd ml_engine
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```
*Note: The `venv/` folder is excluded from Git to keep the repository lightweight.*

### 4. Start Frontend
Open `stitch/stitch/index.html` using **Live Server** in VS Code.

---

## 🛠️ Repository Optimization
To ensure fast deployments on Render and Vercel:
- **`.gitignore`** is configured to exclude large Python virtual environments (`venv/`) and binary models.
- **Docker** is used for the Backend deployment to ensure environment consistency.
- **Vercel** is configured with the Root Directory as `stitch/stitch`.

---

## 📝 Troubleshooting & Maintenance

**1. Vercel "Cannot connect to backend"**
Ensure that the `final_login_page.html` and `user_dashboard.html` files on GitHub have the correct `onrender.com` URLs instead of `localhost`.

**2. ML Engine Build Errors**
If `requirements.txt` is not found, verify that the **Root Directory** in Render is set specifically to `ml_engine`.

**3. Neon Database Idle**
Neon databases may pause after 5 minutes of inactivity. The first request from the website might take 10-15 seconds to "wake up" the database.

---
© 2026 SolarPulse Team | Built with ❤️ for Green Energy.
