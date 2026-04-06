import sys
import re

file_path = r"e:\solar anlyzer\stitch\stitch\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the analysis input box block
old_analysis_block = """<div class="p-2 bg-white/5 backdrop-blur-md border border-white/10 rounded-xl flex flex-col md:flex-row gap-2 max-w-2xl">
<div class="flex-grow flex items-center px-4 gap-3 bg-white/5 rounded-lg border border-white/5">
<span class="material-symbols-outlined text-primary/60">location_on</span>
<input class="bg-transparent border-none focus:ring-0 text-white w-full py-4 font-display" placeholder="Enter your home address..." type="text"/>
</div>
<button id="analyzeNowBtn" class="bg-primary text-background-dark font-bold px-8 py-4 rounded-lg flex items-center justify-center gap-2 hover:bg-white transition-colors group shadow-[0_0_15px_rgba(19,236,91,0.4)]">
                    ANALYZE NOW
                    <span class="material-symbols-outlined group-hover:rotate-45 transition-transform">satellite_alt</span>
</button>
</div>"""
content = content.replace(old_analysis_block, "")

# 2. Remove the 99.2% Accuracy text block
old_accuracy_block = """<div class="mt-4 flex items-center gap-4 text-xs text-slate-400 font-medium px-2">
<span class="flex items-center gap-1"><span class="material-symbols-outlined text-xs text-primary">verified</span> 99.2% Accuracy</span>
<span class="flex items-center gap-1"><span class="material-symbols-outlined text-xs text-primary">bolt</span> 15,000+ Homes Mapped</span>
</div>"""
content = content.replace(old_accuracy_block, "")

# 3. Replace the hidden weatherResults with an initial loading state
old_weather_div = """<div id="weatherResults" class="hidden mt-6 p-6 glass-panel rounded-xl flex-col md:flex-row gap-6 items-center justify-between text-left border-l-4 border-l-primary shadow-2xl">
     <!-- data populated by js -->
</div>"""
new_weather_div = """<div id="weatherResults" class="mt-6 p-6 glass-panel rounded-xl flex flex-col md:flex-row gap-6 items-center justify-between text-left border-l-4 border-l-primary shadow-2xl animate-pulse-glow max-w-2xl">
    <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
            <span class="material-symbols-outlined text-4xl text-primary animate-spin">sync</span>
        </div>
        <div>
            <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Live Telemetry</p>
            <p class="text-xl font-bold text-white">Acquiring GPS coordinates...</p>
        </div>
    </div>
</div>"""
content = content.replace(old_weather_div, new_weather_div)

# 4. Replace the entire <script> logic at the bottom
script_pattern = re.compile(r"<script>\s*const analyzeNowBtn =.*?<\/script>", re.DOTALL)
new_script = """<script>
document.addEventListener("DOMContentLoaded", () => {
    const weatherResults = document.getElementById('weatherResults');
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                try {
                    weatherResults.innerHTML = `
                        <div class="flex items-center gap-4">
                            <div class="w-16 h-16 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
                                <span class="material-symbols-outlined text-4xl text-primary animate-spin">sync</span>
                            </div>
                            <div>
                                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Live Telemetry</p>
                                <p class="text-xl font-bold text-white">Connecting to satellites...</p>
                            </div>
                        </div>
                    `;

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

                    weatherResults.classList.remove("animate-pulse-glow");
                    weatherResults.innerHTML = `
                        <div class="flex items-center gap-4">
                            <div class="w-16 h-16 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
                                <span class="material-symbols-outlined text-4xl text-primary">${icon}</span>
                            </div>
                            <div>
                                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Live Telemetry</p>
                                <p class="text-3xl font-bold text-white">${temp}°C <span class="text-lg font-normal text-slate-300"> &bull; ${condition}</span></p>
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
                } catch (e) {
                    weatherResults.innerHTML = `
                        <div class="flex items-center gap-4">
                            <span class="material-symbols-outlined text-4xl text-red-500">error</span>
                            <div>
                                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Live Telemetry</p>
                                <p class="text-xl font-bold text-red-400">Network connection failed</p>
                            </div>
                        </div>`;
                }
            },
            (error) => {
                weatherResults.innerHTML = `
                    <div class="flex items-center gap-4">
                        <span class="material-symbols-outlined text-4xl text-orange-500">location_off</span>
                        <div>
                            <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Live Telemetry</p>
                            <p class="text-xl font-bold text-orange-400">Location Access Denied</p>
                            <p class="text-xs text-slate-400">Please enable GPS to view live telemetry.</p>
                        </div>
                    </div>`;
            }
        );
    } else {
        weatherResults.innerHTML = `<p class="text-red-500">Geolocation is not supported by your browser.</p>`;
    }
});
</script>"""
content = script_pattern.sub(new_script, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Landing page automated telemetry implemented successfully!")
