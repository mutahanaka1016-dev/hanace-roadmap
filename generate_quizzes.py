import csv
import json
import random

def get_ruby(kanji, kana):
    kanji = kanji.strip()
    kana = kana.strip()
    if not kanji or kanji == kana:
        return kana
    return f"<ruby>{kanji}<rt>{kana}</rt></ruby>"

def load_csv(filename):
    vocab = []
    grammar = []
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = {
                    'kanji': row.get('Kanji', ''),
                    'kana': row.get('Kana', ''),
                    'english': row.get('English', ''),
                    'type': row.get('Type', '')
                }
                if not item['english']:
                    continue
                if row.get('Type') == 'Idiom':
                    grammar.append(item)
                else:
                    vocab.append(item)
    except FileNotFoundError:
        pass
    return vocab, grammar

def load_examples_from_step_data(filename, prefixes):
    examples = []
    try:
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
            for key, val in data.items():
                if any(key.startswith(p) for p in prefixes):
                    for ex in val.get('examples', []):
                        if 'jp' in ex and 'en' in ex:
                            examples.append(ex)
    except Exception as e:
        pass
    return examples

def generate_vocab_questions(level, vocab_items, count=20):
    questions = []
    if not vocab_items:
        return questions
        
    for i in range(count):
        item = vocab_items[i % len(vocab_items)]
        other_meanings = list(set([v['english'] for v in vocab_items if v['english'] != item['english']]))
        random.shuffle(other_meanings)
        options = [item['english']] + other_meanings[:3]
        
        while len(options) < 4:
            options.append("Dummy option")
            
        random.shuffle(options)
        answer_index = options.index(item['english'])
        
        jp_text = get_ruby(item['kanji'], item['kana'])
        
        q = {
            "id": f"{level}_v_{i+1}",
            "category": "vocab",
            "question": f"What is the meaning of '{jp_text}'?",
            "options": options,
            "answer": answer_index,
            "explanation": f"'{jp_text}' means '{item['english']}'."
        }
        questions.append(q)
    return questions

def generate_grammar_questions(level, grammar_items, example_items, count=20):
    questions = []
    
    # Combine idioms and examples to get enough questions
    pool = []
    for g in grammar_items:
        jp_text = get_ruby(g['kanji'], g['kana'])
        pool.append({
            'text': jp_text,
            'english': g['english'],
            'type': 'idiom'
        })
        
    for e in example_items:
        pool.append({
            'text': e['jp'],
            'english': e['en'],
            'type': 'example'
        })
        
    if not pool:
        return questions
        
    for i in range(count):
        item = pool[i % len(pool)]
        other_meanings = list(set([p['english'] for p in pool if p['english'] != item['english']]))
        random.shuffle(other_meanings)
        options = [item['english']] + other_meanings[:3]
        
        while len(options) < 4:
            options.append("Dummy option")
            
        random.shuffle(options)
        answer_index = options.index(item['english'])
        
        if item['type'] == 'idiom':
            question_text = f"What does the grammar pattern '{item['text']}' express?"
            explanation_text = f"'{item['text']}' expresses '{item['english']}'."
        else:
            question_text = f"Translate: '{item['text']}'"
            explanation_text = f"'{item['text']}' translates to '{item['english']}'."
            
        q = {
            "id": f"{level}_g_{i+1}",
            "category": "grammar",
            "question": question_text,
            "options": options,
            "answer": answer_index,
            "explanation": explanation_text
        }
        questions.append(q)
    return questions

# Load Data
beg_v, beg_g = load_csv('/Users/mutahanaka/Desktop/日本語サイト/beginner_vocab.csv')
int_v, int_g = load_csv('/Users/mutahanaka/Desktop/日本語サイト/intermediate_vocab.csv')
adv_v, adv_g = load_csv('/Users/mutahanaka/Desktop/日本語サイト/advanced_vocab.csv')

step_data_file = '/Users/mutahanaka/Desktop/日本語サイト/step_data.json'
beg_ex = load_examples_from_step_data(step_data_file, ['step'])
int_ex = load_examples_from_step_data(step_data_file, ['intStep'])
adv_ex = load_examples_from_step_data(step_data_file, ['pracStep'])

# Generate
all_questions = {
    "beginner": generate_vocab_questions("beginner", beg_v) + generate_grammar_questions("beginner", beg_g, beg_ex),
    "intermediate": generate_vocab_questions("intermediate", int_v) + generate_grammar_questions("intermediate", int_g, int_ex),
    "advanced": generate_vocab_questions("advanced", adv_v) + generate_grammar_questions("advanced", adv_g, adv_ex)
}

js_content = f"const worksheetData = {json.dumps(all_questions, indent=2, ensure_ascii=False)};\n"

with open("/Users/mutahanaka/Desktop/日本語サイト/worksheet_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("worksheet_data.js generated successfully with roadmap content.")
