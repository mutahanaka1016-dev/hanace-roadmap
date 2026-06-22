import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Match both "examples" and examples
examples_blocks = re.findall(r'(?:"examples"|examples)\s*:\s*\[(.*?)\]', html, re.DOTALL)

exact_sentences = {}
pattern = re.compile(r'(?:"jp"|jp)\s*:\s*(?:\'((?:[^\'\\]|\\.)*)\'|"((?:[^"\\]|\\.)*)")')

for block in examples_blocks:
    for match in pattern.finditer(block):
        jp_text = match.group(1) if match.group(1) is not None else match.group(2)
        
        # Strip span tags to get the clean sentence with ruby tags
        raw_jp = re.sub(r'<span class=\\?"tooltip-word\\?".*?>', '', jp_text)
        raw_jp = raw_jp.replace('</span>', '')
        
        # Normalize escaped quotes
        key_text = raw_jp.replace(r'\"', '"').replace(r"\'", "'")
        
        if key_text.strip():
            exact_sentences[key_text] = ""

with open('exact_sentences_map.json', 'w', encoding='utf-8') as f:
    json.dump(exact_sentences, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(exact_sentences)} exact sentences directly from index.html.")
