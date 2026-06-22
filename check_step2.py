import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'pracStep02: (\{.*?"examples": (\[.*?\]).*?"quizzes":)', text, flags=re.DOTALL)
if m:
    examples = json.loads(m.group(2))
    print(examples[0]['jp'])
