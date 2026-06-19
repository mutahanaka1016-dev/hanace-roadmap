import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const lessonData = (\{.*?\});\n\n\s*//', text, re.DOTALL)
data_str = m.group(1)

# we can just regex search for pracStepXX examples
examples = re.findall(r'(pracStep\d+):.*?\"examples\": \[(.*?)\]', data_str, re.DOTALL)

for step, ex_str in examples:
    print(f"=== {step} ===")
    exs = re.findall(r'\{"jp": "(.*?)"', ex_str)
    for ex in exs:
        print(ex)
