import csv
import json

def generate_vocab_html(csv_file):
    html = ""
    types = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word_type = row['Type'].strip()
            if word_type not in types:
                types[word_type] = []
            types[word_type].append(row)
            
    # Define English-Japanese mapping for the types
    type_names = {
        'Noun': '名詞 (Nouns)',
        'I-Adjective': 'い形容詞 (I-Adjectives)',
        'Na-Adjective': 'な形容詞 (Na-Adjectives)'
    }
            
    for t in ['Noun', 'I-Adjective', 'Na-Adjective']:
        if t in types:
            html += f"        <h3 style=\"color: var(--primary-color); border-bottom: 2px solid #efefef; padding-bottom: 10px; font-size: 1.2rem; margin-top: 30px; margin-bottom: 15px;\">{type_names.get(t, t)}</h3>\n"
            html += "        <ul class=\"vocab-list\">\n"
            for row in types[t]:
                kanji = row['Kanji']
                kana = row['Kana']
                english = row['English']
                html += f"            <li class=\"vocab-item\"><div class=\"kana\">{kana}</div><div class=\"kanji\">{kanji}</div><div class=\"meaning\">{english}</div></li>\n"
            html += "        </ul>\n"
            
    return html

html_content = generate_vocab_html('/Users/mutahanaka/Desktop/日本語サイト/beginner_vocab.csv')

with open('/Users/mutahanaka/Desktop/日本語サイト/vocab_part.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
