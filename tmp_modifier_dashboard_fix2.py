import sys
import re

file_path = r"e:\solar anlyzer\stitch\stitch\user_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We look for the tailwind script opening tag up to its closing tag (line 6 to line 56)
match = re.search(r'(<script src="https://cdn.tailwindcss.com\?plugins=forms,container-queries">)(.*?)(</script>)', content, re.DOTALL)

if match:
    injected_js = match.group(2)
    # Restore the tailwind script properly
    restored_tailwind = '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>\n'
    
    full_bad_block = match.group(0)
    
    # Replace the bad block with just the tailwind tag
    content = content.replace(full_bad_block, restored_tailwind)
    
    # Put the extracted JS at the bottom of the file
    content = content.replace("</body>", f"<script>{injected_js}</script>\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed user_dashboard.html successfully!")
else:
    print("Could not find the broken tag.")
