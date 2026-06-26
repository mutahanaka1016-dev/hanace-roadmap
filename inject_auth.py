import os
import glob

html_files = glob.glob("*.html")
auth_script = '<script src="auth.js" type="module"></script>\n'

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'src="auth.js"' in content:
        continue
        
    # Find the <head> tag and inject the script right after it
    if '<head>' in content:
        content = content.replace('<head>', '<head>\n    ' + auth_script, 1)
    elif '<HEAD>' in content:
        content = content.replace('<HEAD>', '<HEAD>\n    ' + auth_script, 1)
    else:
        # Fallback: put it before first <script> or at the top
        content = auth_script + content
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Injected auth.js into {len(html_files)} files.")
