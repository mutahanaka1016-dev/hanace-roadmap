import json
import re

with open('step_data.json', 'r', encoding='utf-8') as f:
    steps = json.load(f)

# Extract all japanese sentences
all_jps = []
for step_id, data in steps.items():
    for ex in data.get('examples', []):
        jp = ex.get('jp', '')
        if jp:
            all_jps.append(jp)

# Clean out ruby tags to see raw text
def remove_ruby(text):
    return re.sub(r'<rt>.*?</rt>', '', text).replace('<ruby>', '').replace('</ruby>', '')

unique_sentences = set()
for jp in all_jps:
    # remove html spans if they exist from my previous edit
    jp = re.sub(r'<span[^>]*>', '', jp)
    jp = jp.replace('</span>', '')
    unique_sentences.add(remove_ruby(jp))

with open('unique_sentences.txt', 'w', encoding='utf-8') as f:
    for s in sorted(list(unique_sentences)):
        f.write(s + '\n')

print(f"Extracted {len(unique_sentences)} unique sentences.")
