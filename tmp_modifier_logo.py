import sys

file_path = r"e:\solar anlyzer\stitch\stitch\user_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_logo_block = """<div class="flex items-center gap-2">
<div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
<span class="material-icons text-background-dark font-bold">wb_sunny</span>
</div>
<span class="text-xl font-bold tracking-tight text-slate-900 dark:text-white uppercase">Helio<span class="text-primary">Scan</span></span>
</div>"""

new_logo_block = """<div class="flex items-center gap-2">
<div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
<span class="material-symbols-outlined text-background-dark font-bold">solar_power</span>
</div>
<span class="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Solar<span class="text-primary">Pulse</span></span>
</div>"""

# Replace the specific old string
content = content.replace(old_logo_block, new_logo_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Branding update to SolarPulse applied successfully!")
