import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const lessonData = (\{.*?\});\n\n\s*//', html, re.DOTALL)
data_str = m.group(1)

# try to convert it to valid JSON to parse it
# the keys are unquoted, e.g. step01: {
# we can use a regex to quote them
data_str_json = re.sub(r'([a-zA-Z0-9_]+):\s*\{', r'"\1": {', data_str)
# also quizzes:, vocabulary:, etc might be unquoted? No, my script output them with quotes. But original step01 has unquoted keys.
# Let's just find any `key: ` and quote it.
data_str_json = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', data_str_json)

try:
    data = json.loads(data_str_json)
    print("Parsed JSON successfully.")
except Exception as e:
    print("JSON parse error:", e)

