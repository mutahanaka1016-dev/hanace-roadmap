import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the half-width parenthesis in the UI to full-width
text = text.replace("'(' + word.kana + ')'", "'（' + word.kana + '）'")

def replace_vocab(m):
    step_id = m.group(1)
    vocab_str = m.group(2)
    vocab = json.loads(vocab_str)
    
    for v in vocab:
        if v['kanji'] == '受かる': v['kana'] = 'うかる'
        if v['kanji'] == '親切な': v['kana'] = 'しんせつな'
        if v['kanji'] == '割れる': v['kana'] = 'われる'
        if v['kanji'] == '壊す': v['kana'] = 'こわす'
        
    return f'"{step_id}": {json.dumps(vocab, ensure_ascii=False)}' # This is not safe since regex captured whole block

# Actually, let's just do simple string replacements for the JSON data since they are unique enough
text = text.replace('"kana": "受かる", "kanji": "受かる"', '"kana": "うかる", "kanji": "受かる"')
text = text.replace('"kana": "親切な", "kanji": "親切な"', '"kana": "しんせつな", "kanji": "親切な"')
text = text.replace('"kana": "割れる", "kanji": "割れる"', '"kana": "われる", "kanji": "割れる"')
text = text.replace('"kana": "壊す", "kanji": "壊す"', '"kana": "こわす", "kanji": "壊す"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed kana and parenthesis in index.html!")
