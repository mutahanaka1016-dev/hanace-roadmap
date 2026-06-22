import json

with open('step_data.json', 'r', encoding='utf-8') as f:
    steps = json.load(f)

exact_sentences = {}
for step_id, data in steps.items():
    for ex in data.get('examples', []):
        jp = ex.get('jp', '')
        if jp:
            exact_sentences[jp] = ""

with open('exact_sentences_map.json', 'w', encoding='utf-8') as f:
    json.dump(exact_sentences, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(exact_sentences)} exact sentences.")
