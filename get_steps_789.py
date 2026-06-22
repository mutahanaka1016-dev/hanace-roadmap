import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for step in [7, 8, 9]:
    m = re.search(fr'pracStep{step:02d}: (\{{.*?"examples": (\[.*?\]).*?"quizzes":)', text, flags=re.DOTALL)
    if m:
        examples = json.loads(m.group(2))
        for i, ex in enumerate(examples):
            print(f"Step {step} Ex {i}: {ex['jp']}")
