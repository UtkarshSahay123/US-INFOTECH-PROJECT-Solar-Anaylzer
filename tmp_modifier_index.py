import sys

file_path = r"e:\solar anlyzer\stitch\stitch\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Modify the button to have an ID
old_btn = """<button class="bg-primary text-background-dark font-bold px-8 py-4 rounded-lg flex items-center justify-center gap-2 hover:bg-white transition-colors group">
                    ANALYZE NOW
                    <span class="material-symbols-outlined group-hover:rotate-45 transition-transform">satellite_alt</span>
</button>"""
new_btn = """<button id="analyzeNowBtn" class="bg-primary text-background-dark font-bold px-8 py-4 rounded-lg flex items-center justify-center gap-2 hover:bg-white transition-colors group shadow-[0_0_15px_rgba(19,236,91,0.4)]">
                    ANALYZE NOW
                    <span class="material-symbols-outlined group-hover:rotate-45 transition-transform">satellite_alt</span>
</button>"""
content = content.replace(old_btn, new_btn)

# 2. Add the results div just below that entire div section
target_anchor = """</div>
<div class="mt-4 flex items-center gap-4 text-xs text-slate-400 font-medium px-2">"""

results_div = """</div>
<div id="weatherResults" class="hidden mt-6 p-6 glass-panel rounded-xl flex-col md:flex-row gap-6 items-center justify-between text-left border-l-4 border-l-primary shadow-2xl">
     <!-- data populated by js -->
</div>
<div class="mt-4 flex items-center gap-4 text-xs text-slate-400 font-medium px-2">"""
content = content.replace(target_anchor, results_div)

# 3. Inject JS script before </body>
js_logic = """
<script>
const analyzeNowBtn = document.getElementById('analyzeNowBtn');
const weatherResults = document.getElementById('weatherResults');

if (analyzeNowBtn) {
    analyzeNowBtn.addEventListener('click', () => {
        analyzeNowBtn.innerHTML = `LOCATING <span class="material-symbols-outlined animate-spin">sync</span>`;
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    
                    try {
                        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=sunrise,sunset&current_weather=true&timezone=auto`;
                        const res = await fetch(url);
                        const data = await res.json();
                        
                        const current = data.current_weather;
                        const daily = data.daily;
                        
                        const temp = current.temperature;
                        
                        // Format time
                        const sunriseRaw = new Date(daily.sunrise[0]);
                        const sunsetRaw = new Date(daily.sunset[0]);
                        const options = { hour: '2-digit', minute:'2-digit' };
                        const sunrise = sunriseRaw.toLocaleTimeString([], options);
                        const sunset = sunsetRaw.toLocaleTimeString([], options);
                        
                        // Decode weather code
                        const weatherCode = current.weathercode;
                        let condition = "Sunny";
                        let icon = "clear_day";
                        if (weatherCode > 0 && weatherCode <= 3) { condition="Partly Cloudy"; icon="partly_cloudy_day"; }
                        else if (weatherCode > 3 && weatherCode <= 67) { condition="Rainy"; icon="rainy"; }
                        else if (weatherCode > 67) { condition="Snow/Storm"; icon="ac_unit"; }

                        weatherResults.innerHTML = `
                            <div class="flex items-center gap-4">
                                <div class="w-16 h-16 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
                                    <span class="material-symbols-outlined text-4xl text-primary">${icon}</span>
                                </div>
                                <div>
                                    <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Live Telemetry</p>
                                    <p class="text-3xl font-bold text-white">${temp}°C <span class="text-lg font-normal text-slate-300"> • ${condition}</span></p>
                                </div>
                            </div>
                            <div class="hidden md:block w-px h-16 bg-white/10"></div>
                            <div class="flex gap-10">
                                <div>
                                    <p class="text-xs text-primary font-bold uppercase tracking-widest mb-1 flex items-center gap-1"><span class="material-symbols-outlined text-sm">wb_twilight</span>Sunrise</p>
                                    <p class="text-2xl font-bold text-white">${sunrise}</p>
                                </div>
                                <div>
                                    <p class="text-xs text-orange-400 font-bold uppercase tracking-widest mb-1 flex items-center gap-1"><span class="material-symbols-outlined text-sm">clear_night</span>Sunset</p>
                                    <p class="text-2xl font-bold text-white">${sunset}</p>
                                </div>
                            </div>
                        `;
                        weatherResults.classList.remove('hidden');
                        weatherResults.classList.add('flex');
                        analyzeNowBtn.innerHTML = `ANALYSIS ACTIVE <span class="material-symbols-outlined text-background-dark">satellite_alt</span>`;
                        analyzeNowBtn.classList.add('bg-white'); // indicates success visually
                    } catch (e) {
                        analyzeNowBtn.innerHTML = `NETWORK ERROR <span class="material-symbols-outlined text-background-dark">error</span>`;
                    }
                },
                (error) => {
                    analyzeNowBtn.innerHTML = `GPS DENIED <span class="material-symbols-outlined text-background-dark">location_off</span>`;
                    alert("Please allow location access to calculate solar potential for your specific coordinates.");
                }
            );
        } else {
            analyzeNowBtn.innerHTML = `UNSUPPORTED <span class="material-symbols-outlined text-red-500">error</span>`;
        }
    });
}
</script>
</body>
"""
content = content.replace("</body>", js_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Weather Display panel implemented on index.html!")
