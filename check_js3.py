import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const lessonData = (\{.*?\});\n\n\s*//', text, re.DOTALL)
print("Found lessonData:" , m is not None)
