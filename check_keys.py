import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const lessonData = (\{.*?\});\n\n\s*//', html, re.DOTALL)
if m:
    data_str = m.group(1)
    # The JSON is not strict JSON because keys are not quoted. (e.g. `step01: {`)
    print("Found lessonData")
    # Let's extract all "kana" and "kanji" fields from pracStep
    import re
    kanas = re.findall(r'"kana": "(.*?)"', html)
    kanjis = re.findall(r'"kanji": "(.*?)"', html)
    
    for word in kanas + kanjis:
        if word and re.search(r'[?*+()\[\]{}|\\^$]', word):
            print(f"SPECIAL CHAR IN WORD: {word}")
else:
    print("Could not find lessonData")
