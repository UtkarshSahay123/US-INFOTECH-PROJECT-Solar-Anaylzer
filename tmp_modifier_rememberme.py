import sys
import glob
import os
import re

html_files = glob.glob(r"E:\solar anlyzer\stitch\stitch\*.html")

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Update final_login_page.html
    if "final_login_page.html" in filepath or "login" in content.lower():
        # Add id to checkbox
        if '<input class="rounded border-[#cfe7d7] text-primary focus:ring-primary" type="checkbox"/>' in content:
            content = content.replace('<input class="rounded border-[#cfe7d7] text-primary focus:ring-primary" type="checkbox"/>', '<input id="rememberMe" class="rounded border-[#cfe7d7] text-primary focus:ring-primary" type="checkbox"/>')
            modified = True

        # Check JS
        old_login_js = """            if (response.ok) {
                // Success! Token received. Save to Browser & Redirect
                localStorage.setItem("token", data.token);
                window.location.href = "user_dashboard.html"; 
            }"""
        new_login_js = """            if (response.ok) {
                const rememberMe = document.getElementById('rememberMe').checked;
                // Success! Token received. Save to Browser & Redirect
                if (rememberMe) {
                    localStorage.setItem("token", data.token);
                    sessionStorage.removeItem("token");
                } else {
                    sessionStorage.setItem("token", data.token);
                    localStorage.removeItem("token");
                }
                window.location.href = "user_dashboard.html"; 
            }"""
        if old_login_js in content:
            content = content.replace(old_login_js, new_login_js)
            modified = True

    # 2. Update user_dashboard.html (and others) token fetching
    # Replace `localStorage.getItem('token')` with `(localStorage.getItem('token') || sessionStorage.getItem('token'))`
    # Replace `localStorage.removeItem('token')` with `localStorage.removeItem('token'); sessionStorage.removeItem('token')`
    
    # We will use regex to do it safely
    # First, getter
    if "localStorage.getItem('token')" in content or 'localStorage.getItem("token")' in content:
        content = content.replace("localStorage.getItem('token')", "(localStorage.getItem('token') || sessionStorage.getItem('token'))")
        content = content.replace('localStorage.getItem("token")', '(localStorage.getItem("token") || sessionStorage.getItem("token"))')
        modified = True
        
    # Second, setter/remover in logout
    # Check for logout logic
    if "localStorage.removeItem('token')" in content:
        content = content.replace("localStorage.removeItem('token')", "localStorage.removeItem('token'); sessionStorage.removeItem('token');")
        modified = True
    if 'localStorage.removeItem("token")' in content:
        content = content.replace('localStorage.removeItem("token")', 'localStorage.removeItem("token"); sessionStorage.removeItem("token");')
        modified = True


    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated logic in {os.path.basename(filepath)}")
