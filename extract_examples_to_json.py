import re
import json

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find all jp fields in examples arrays
pattern = r"examples\s*:\s*\[(.*?)\]"
matches = re.findall(pattern, text, flags=re.DOTALL)

examples = []
for m in matches:
    jp_pattern = r"jp\s*:\s*['\"](.*?)['\"]"
    jps = re.findall(jp_pattern, m)
    for jp in jps:
        examples.append(jp)

with open("all_examples.json", "w", encoding="utf-8") as f:
    json.dump(examples, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(examples)} examples.")
