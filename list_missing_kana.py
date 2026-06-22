import json

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'pracStep(\d{2}): (\{.*?"videoUrl".*?"vocabulary": \[.*?\])', text, flags=re.DOTALL)

for m in matches:
    step = m.group(1)
    vocab_str = re.search(r'"vocabulary": (\[.*?\])', m.group(2), flags=re.DOTALL).group(1)
    vocab = json.loads(vocab_str)
    for v in vocab:
        if v['kanji'] == v['kana'] and any('\u4e00' <= c <= '\u9fff' for c in v['kanji']):
            print(f"Missing kana for: {v['kanji']}")
