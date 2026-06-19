import re
import json

quizzes_data = {
    "pracStep01": [
        {"question": "Which particle marks new information or the subject of a subordinate clause?", "options": ["が", "は", "を", "に"], "answer": 0},
        {"question": "Which particle is used for contrast?", "options": ["は", "が", "に", "で"], "answer": 0}
    ],
    "pracStep02": [
        {"question": "How do you ask 'Which one is more...'?", "options": ["どちらのほうが", "どれ", "だれ", "どこ"], "answer": 0},
        {"question": "How do you say 'A is not as good as B'?", "options": ["AはBほどよくない", "AはBよりいい", "AとBは同じ", "BはAほどよくない"], "answer": 0}
    ],
    "pracStep03": [
        {"question": "What is the potential form of 食べる?", "options": ["食べられる", "食べる", "食べた", "食べない"], "answer": 0},
        {"question": "What is the potential form of 行く?", "options": ["行ける", "行かれる", "行きたい", "行こう"], "answer": 0}
    ],
    "pracStep04": [
        {"question": "Which word is often used with conditional forms to mean 'If by any chance'?", "options": ["もし", "いつも", "まだ", "もう"], "answer": 0},
        {"question": "Which conditional is often used for giving contextual advice?", "options": ["なら", "と", "ば", "て"], "answer": 0}
    ],
    "pracStep05": [
        {"question": "Which conjunction means 'What\\'s more / Moreover'?", "options": ["しかも", "けれど", "だから", "すると"], "answer": 0},
        {"question": "Which conjunction is used for contrast ('However')?", "options": ["けれど", "それで", "だから", "さらに"], "answer": 0}
    ],
    "pracStep06": [
        {"question": "Which idiom means 'to do something in advance'?", "options": ["〜ておく", "〜てしまう", "〜てある", "〜ている"], "answer": 0},
        {"question": "Which idiom means 'to complete something' or 'to do regrettably'?", "options": ["〜てしまう", "〜ておく", "〜てある", "〜ている"], "answer": 0}
    ],
    "pracStep07": [
        {"question": "Which is the humble form of 'to receive'?", "options": ["いただく", "くださる", "さしあげる", "もらう"], "answer": 0},
        {"question": "Which is the honorific form of 'to give' (someone gives to me)?", "options": ["くださる", "いただく", "さしあげる", "くれる"], "answer": 0}
    ],
    "pracStep08": [
        {"question": "Which is the intransitive verb for 'to break'?", "options": ["壊れる", "壊す", "落ちる", "落とす"], "answer": 0},
        {"question": "The sentence '窓が開けてあります' uses which type of verb?", "options": ["Transitive", "Intransitive", "Passive", "Causative"], "answer": 0}
    ],
    "pracStep09": [
        {"question": "Which phrase indicates hearsay (I heard that...)?", "options": ["〜そうです (Dictionary form +)", "〜みたいです", "〜はずです", "〜そうです (Stem +)"], "answer": 0},
        {"question": "'雨が降りそうです' means?", "options": ["It looks like it will rain", "I heard it will rain", "It is raining", "It rained"], "answer": 0}
    ],
    "pracStep10": [
        {"question": "What is the passive form of 食べる?", "options": ["食べられる", "食べさせる", "食べさせられる", "食べたい"], "answer": 0},
        {"question": "What form is '練習させられました' (was forced to practice)?", "options": ["Causative-Passive", "Passive", "Causative", "Potential"], "answer": 0}
    ],
    "pracStep11": [
        {"question": "What is the honorific form of 食べる?", "options": ["召し上がる", "いただく", "おっしゃる", "参る"], "answer": 0},
        {"question": "What is the humble form of 言う?", "options": ["申す", "おっしゃる", "伺う", "拝見する"], "answer": 0}
    ],
    "pracStep12": [
        {"question": "What phrase is often used to apologize for inconvenience?", "options": ["ご迷惑をおかけしました", "お世話になっております", "ありがとうございます", "かしこまりました"], "answer": 0},
        {"question": "How do you formally say 'Due to ~' or 'Because of ~'?", "options": ["〜のため", "〜にもかかわらず", "〜だから", "〜から"], "answer": 0}
    ],
    "pracStep13": [
        {"question": "What phrase means 'I think / consider that ~' in a formal discussion?", "options": ["〜と考えます", "〜かもしれません", "〜べきです", "〜でしょう"], "answer": 0},
        {"question": "How do you say 'Therefore'?", "options": ["したがって", "なぜなら", "けれど", "しかも"], "answer": 0}
    ]
}

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

for step, quizzes in quizzes_data.items():
    # Find the block for the step. We will find "quizzes": [] inside that block.
    # To do this safely, we will look for `step + r': \{.*?"quizzes"\s*:\s*\[\s*\]\s*\}'`
    pattern = r'(' + step + r':\s*\{.*?"quizzes"\s*:\s*)\[\s*\](\s*\})'
    
    quiz_str = json.dumps(quizzes, ensure_ascii=False)
    
    # Check if the step exists and has empty quizzes
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, r'\1' + quiz_str + r'\2', text, count=1, flags=re.DOTALL)
        print(f"Updated {step}")
    else:
        print(f"Could not find or update {step}")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Done.")
