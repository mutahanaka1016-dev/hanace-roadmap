import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'pracStep09: (\{.*?"examples": (\[.*?\]).*?"quizzes":)', text, flags=re.DOTALL)
if m:
    print(m.group(2))
