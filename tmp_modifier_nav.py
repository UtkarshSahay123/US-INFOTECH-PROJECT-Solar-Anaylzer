import re

files = [
    r"e:\solar anlyzer\stitch\stitch\final_login_page.html",
    r"e:\solar anlyzer\stitch\stitch\signup_page.html"
]

nav_template = """
<nav class="fixed top-0 w-full z-50 bg-[#0a120d]/90 backdrop-blur-md border-b border-white/10 hidden lg:block">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
<div class="flex justify-between h-20 items-center">
<a href="index.html" class="flex items-center gap-2 cursor-pointer no-underline">
<div class="w-10 h-10 bg-[#13ec5b] rounded-lg flex items-center justify-center">
<span class="material-symbols-outlined text-[#102216] font-bold">solar_power</span>
</div>
<span class="text-2xl font-bold tracking-tight text-white mb-0">Solar<span class="text-[#13ec5b]">Pulse</span></span>
</a>
<div class="hidden md:flex items-center space-x-8">
<a class="text-sm font-medium text-slate-300 hover:text-[#13ec5b] transition-colors no-underline" href="index.html">Home</a>
<a class="text-sm font-medium text-slate-300 hover:text-[#13ec5b] transition-colors no-underline" href="final_login_page.html">Login</a>
<a class="text-sm font-medium text-slate-300 hover:text-[#13ec5b] transition-colors no-underline" href="technology_page.html">Technology</a>
</div>
</div>
</div>
</nav>
"""

# Helper to remove old absolute SolarPlatform icons
def strip_old_icon(content):
    # final_login_page.html icon removal
    res = re.sub(r'<div class="absolute top-10 left-10 flex items-center gap-2">.*?</h2>\s*</div>', '', content, flags=re.DOTALL)
    # signup_page.html icon removal
    res = re.sub(r'<div class="flex items-center gap-2 mb-8">\s*<span class="material-icons text-4xl">wb_sunny</span>\s*<span class="text-2xl font-bold tracking-tight">SolarPlatform</span>\s*</div>', '', res, flags=re.DOTALL)
    # Remove mobile inline ones if they conflict, actually let's leave mobile since the nav is hidden lg:block
    return res

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: Remove old manual icons
    content = strip_old_icon(content)

    # Step 2: Inject Nav directly after <body ...>
    if "<nav class=" not in content:
        # Avoid duplicate injections
        content = re.sub(r'(<body[^>]*>)', r'\1' + nav_template, content, count=1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Navured:", path)

