import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const lessonData = (\{.*?\});\n\n\s*//', html, re.DOTALL)
data_str = m.group(1)
lines = data_str.split('\n')
for i, line in enumerate(lines[:10]):
    print(f"Line {i+1}: {line}")

