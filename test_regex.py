import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'(pracStep\d{2}):\s*(\{.*?)"examples":\s*\[(.*?)\]', text, flags=re.DOTALL)
print(f"Found {len(matches)} matches.")
if len(matches) > 0:
    print("Match 1:", matches[0][0])
