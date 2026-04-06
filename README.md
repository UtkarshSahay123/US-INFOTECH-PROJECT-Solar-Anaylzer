# ☀️ SolarPulse (Solar Analyzer)

**SolarPulse** is a full-stack, AI-powered platform for assessing solar panel feasibility. By utilizing computer vision (YOLOv8) to analyze rooftop imagery, calculating highly accurate solar potential, and tracking historical analyses using a robust Spring Boot backend, SolarPulse empowers seamless green energy planning.

---

## 🏗️ Architecture Stack

The project operates through a secure 3-tier microservice architecture:

| Tier | Path | Tech Stack | Port | Purpose |
|------|------|------------|------|---------|
| **1. Frontend Interface** | `\stitch\stitch` | HTML5, Tailwind CSS, Vanilla JS | `5500` (Live Server) | UI/UX, Dynamic rendering, Form state |
| **2. Auth & Data Backend**| `\stitch\authentication\authentication\demo` | Java 17, Spring Boot, Spring Security, PostgreSQL | `8080` | JWT Auth, OAuth2 (Google/MS), Data Persistence, OTP Emails |
| **3. ML & Vision Engine** | `\ml_engine` | Python 3, FastAPI, YOLOv8 (Ultralytics), OpenCV | `8000` | Image Segmentation, Area calculation, Weather data integration |

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

## 🚀 How to Run the Project Locally

Because the project relies on microservices, you **must run all 3 servers simultaneously** for the application to function.

### 1. Database Setup
Ensure **PostgreSQL** is running on your machine on port `5432`.
- Username: `postgres`
- Password: `root`
- Database Name: `solar_analyzer_auth` *(Spring Boot will automatically create tables inside it)*

### 2. Start the Auth & Data Backend (Spring Boot)
This server handles logins, saves data, and issues tokens.
1. Open a terminal and navigate to the backend folder:
   ```bash
   cd "e:\solar anlyzer\stitch\authentication\authentication\demo"
   ```
2. Start the server using Maven:
   ```bash
   .\mvnw.cmd spring-boot:run
   ```
   *Expect to see: `Started SolarAnalyzerAuthenticationApplication` on port `8080`.*

### 3. Start the ML Engine (Python FastAPI)
This server processes images and computes formulas.
1. Open a **second** terminal and navigate to the python folder:
   ```bash
   cd "e:\solar anlyzer\ml_engine"
   ```
2. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. Start the Uvicorn server:
   ```bash
   uvicorn main:app --reload
   ```
   *Expect to see: `Uvicorn running on http://127.0.0.1:8000`.*

### 4. Start the Frontend (UI)
The frontend communicates with both the `:8000` and `:8080` servers.
1. Open **VS Code**.
2. Open the frontend folder: `e:\solar anlyzer\stitch\stitch`
3. Right-click on `index.html` and select **"Open with Live Server"**.
4. The application will launch in your browser (usually at `http://localhost:5500/index.html`).

---

## 🔧 Environment Configuration

If you deploy this to production or switch machines, update the secrets in:
`e:\solar anlyzer\stitch\authentication\authentication\demo\src\main\resources\application.properties`

- **Database Credentials**: `spring.datasource.username` / `password`
- **Email OTP Senders**: `spring.mail.username` / `password` (Requires Gmail App Password)
- **OAuth2 Secrets**: `spring.security.oauth2.client.registration...client-secret`

---

## 🛠️ Troubleshooting

**1. "Port 8080 was already in use"**
A ghost Spring Boot process is stuck in the background. Kill it via PowerShell:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess | Stop-Process -Force
```

**2. 401 Unauthorized Error on Dashboard Save**
Ensure you aren't manually browsing to the `user_dashboard.html` without logging in. Let `final_login_page.html` redirect you properly so it can store the JWT token correctly.

**3. "No such option: --reload." in Python Uvicorn**
Verify you do not have a trailing period. The correct command is: `uvicorn main:app --reload` (no grammar at the end).
