import sys

file_path = r"e:\solar anlyzer\stitch\stitch\user_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I will find the block I injected into the tailwind script and remove it, putting the tailwind script back.
bad_tailwind = """<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries">

    window.deleteHistoryItem = async function(id, event) {"""

# If we find this, let's extract the injected code up to the next `</script>`
import re

# We injected `\n    window.deleteHistoryItem = ... </script>\n`
match = re.search(r'(<script src="https://cdn.tailwindcss.com\?plugins=forms,container-queries">)(.*?)(</script>\n)', content, re.DOTALL)

if match:
    # the middle part is the injected JS
    injected_js = match.group(2)
    # Restore the tailwind script completely:
    restored_tailwind = `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>\n`
    
    # We replace the entire matched block with just the restored tailwind script
    full_bad_block = match.group(1) + match.group(2) + match.group(3)
    content = content.replace(full_bad_block, restored_tailwind)
    
    # Now append the injected JS to the VERY END of the file, right before </body>
    if "</body>" in content:
        content = content.replace("</body>", f"<script>{injected_js}</script>\n</body>")
    else:
        # fallback
        content += f"\n<script>{injected_js}</script>\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed user_dashboard.html!")
else:
    print("Match not found.")
