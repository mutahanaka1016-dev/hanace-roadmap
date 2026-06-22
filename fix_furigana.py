import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    # Step 7
    "先生": "<ruby>先生<rt>せんせい</rt></ruby>",
    "私": "<ruby>私<rt>わたし</rt></ruby>",
    "今度": "<ruby>今度<rt>こんど</rt></ruby>",
    "引っ越す": "<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>す",
    "手伝って": "<ruby>手伝<rt>てつだ</rt></ruby>って",
    
    # Step 8
    "おもちゃ": "おもちゃ", # No kanji
    "壊れました": "<ruby>壊<rt>こわ</rt></ruby>れました",
    "壊しました": "<ruby>壊<rt>こわ</rt></ruby>しました",
    "窓": "<ruby>窓<rt>まど</rt></ruby>",
    "開けてあります": "<ruby>開<rt>あ</rt></ruby>けてあります",
    "開いています": "<ruby>開<rt>あ</rt></ruby>いています",

    # Step 9
    "雨": "<ruby>雨<rt>あめ</rt></ruby>",
    "降りそう": "<ruby>降<rt>ふ</rt></ruby>りそう",
    "来年": "<ruby>来年<rt>らいねん</rt></ruby>",
    "会社": "<ruby>会社<rt>かいしゃ</rt></ruby>",
    "移動するそう": "<ruby>移動<rt>いどう</rt></ruby>するそう",
    "彼女": "<ruby>彼女<rt>かのじょ</rt></ruby>",
    "来週": "<ruby>来週<rt>らいしゅう</rt></ruby>",
    "結婚するらしい": "<ruby>結婚<rt>けっこん</rt></ruby>するらしい",
    "携帯": "<ruby>携帯<rt>けいたい</rt></ruby>",
    "連絡": "<ruby>連絡<rt>れんらく</rt></ruby>",
    "風邪": "<ruby>風邪<rt>かぜ</rt></ruby>",
}

def replace_examples(m):
    step_id_str = m.group(1)
    step = int(step_id_str)
    
    if step not in [7, 8, 9]:
        return m.group(0)
        
    examples_str = m.group(3)
    try:
        examples = json.loads(examples_str)
        for ex in examples:
            jp = ex['jp']
            
            # Since some replacements might match inside tags or already replaced ones,
            # it's best to be careful. But these are distinct kanji.
            # Except we need to avoid replacing inside `<ruby>先生<rt>せんせい</rt></ruby>`.
            # If the string doesn't have `<ruby>`, we can safely replace.
            
            for k, v in replacements.items():
                # Only replace if not already ruby'd
                # A simple regex to replace kanji not preceded by > or <ruby>
                # Actually, since we know they don't have <ruby>, we can just replace.
                if k in jp and f"<ruby>{k[0]}" not in jp:
                    jp = jp.replace(k, v)
            
            ex['jp'] = jp
        
        new_examples_str = json.dumps(examples, ensure_ascii=False)
        return m.group(0).replace(examples_str, new_examples_str)
    except json.JSONDecodeError as e:
        print("JSON Error", e)
        return m.group(0)

new_text = re.sub(r'pracStep(\d{2}): (\{.*?"examples": (\[.*?\]).*?"quizzes":)', replace_examples, text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Added furigana to Steps 7, 8, 9!")
