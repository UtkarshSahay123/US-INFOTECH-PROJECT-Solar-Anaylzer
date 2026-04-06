import sys

file_path = r"e:\solar anlyzer\stitch\stitch\signup_page.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_bars = """<div class="mt-2 flex gap-1">
<div class="h-1 flex-1 bg-primary rounded-full"></div>
<div class="h-1 flex-1 bg-primary rounded-full"></div>
<div class="h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full"></div>
<div class="h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full"></div>
</div>
<p class="text-[11px] text-slate-500 mt-1">Password strength: <span class="text-primary font-semibold">Medium</span></p>"""

new_bars = """<div class="mt-2 flex gap-1" id="strengthBars">
<div class="h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full transition-colors duration-300 shadow-sm"></div>
<div class="h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full transition-colors duration-300 shadow-sm"></div>
<div class="h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full transition-colors duration-300 shadow-sm"></div>
<div class="h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full transition-colors duration-300 shadow-sm"></div>
</div>
<p class="text-[11px] text-slate-500 mt-1">Password strength: <span id="strengthText" class="font-semibold text-slate-400">None</span></p>"""

content = content.replace(old_bars, new_bars)

js_start = "<script>"
js_addition = """<script>
    // Live Password Strength Checker
    document.getElementById('password').addEventListener('input', function(e) {
        const val = e.target.value;
        const bars = document.getElementById('strengthBars').children;
        const text = document.getElementById('strengthText');
        
        let strength = 0;
        if (val.length >= 6) strength++;
        if (val.length >= 8 && /[A-Z]/.test(val)) strength++;
        if (val.length >= 8 && /[0-9]/.test(val)) strength++;
        if (val.length >= 8 && /[^A-Za-z0-9]/.test(val)) strength++;

        // Reset bars
        for (let i = 0; i < 4; i++) {
            bars[i].className = "h-1 flex-1 bg-slate-200 dark:bg-slate-700 rounded-full transition-colors duration-300";
        }
        
        // Apply colors mathematically based on strength score
        if (val.length === 0) {
            text.textContent = 'None';
            text.className = 'font-semibold text-slate-400';
        } else if (strength <= 1) {
            bars[0].classList.replace('bg-slate-200', 'bg-red-500');
            bars[0].classList.replace('dark:bg-slate-700', 'bg-red-500');
            text.textContent = 'Weak';
            text.className = 'font-semibold text-red-500';
        } else if (strength === 2) {
            for(let i=0; i<2; i++) {
                bars[i].classList.replace('bg-slate-200', 'bg-yellow-500');
                bars[i].classList.replace('dark:bg-slate-700', 'bg-yellow-500');
            }
            text.textContent = 'Fair';
            text.className = 'font-semibold text-yellow-500';
        } else if (strength === 3) {
            for(let i=0; i<3; i++) {
                bars[i].classList.replace('bg-slate-200', 'bg-primary');
                bars[i].classList.replace('dark:bg-slate-700', 'bg-primary');
            }
            text.textContent = 'Good';
            text.className = 'font-semibold text-primary';
        } else if (strength >= 4) {
            for(let i=0; i<4; i++) {
                bars[i].classList.replace('bg-slate-200', 'bg-green-500');
                bars[i].classList.replace('dark:bg-slate-700', 'bg-green-500');
            }
            text.textContent = 'Strong';
            text.className = 'font-semibold text-green-500';
        }
    });
"""

# inject logic into the script block
content = content.replace(js_start, js_addition, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Live password checker script created and injected!")
