import re
import json

raw_data = """
STEP 1
vocabulary

何か / Something
実は / Actually / In fact
おじいさん / Grandfather / Old man
主語 / Subject (grammar)
新情報（しんじょうほう） / New Information
疑問詞（ぎもんし） / Question Words
不思議（ふしぎ） / Mysterious
交番（こうばん） / Police Box
会議室（かいぎしつ） / Meeting Room
選ぶ（えらぶ） / To choose
見つかる（みつかる） / To be found
昔々（むかしむかし） / Once upon a time

STEP 2
vocabulary

比較（ひかく） / Comparisons
より / Than (used in comparison)
上手くなる（うまくなる） / To improve
便利になる（べんりになる） / To become convenient
怠ける（なまける） / To be lazy
どちらのほうが / Which is more
背が高い（せがたかい） / Tall (stature)
一番 / The most / Number one
頭がいい（あたまがいい） / Smart
世界（せかい） / World
人間（にんげん） / Human
公共交通（こうきょうこうつう） / Public transportation

STEP 3
vocabulary

能力（のうりょく） / Ability
可能性（かのうせい） / Possibility
運転する（うんてんする） / To drive
はじめは / At first
残念（ざんねん） / Unfortunately
ぺらぺら / Fluent
漢字（かんじ） / Kanji
泳ぐ（およぐ） / To swim
弾く（ひく） / To play (piano/guitar)
テニスする / To play tennis
少し / A little / A bit
子どものころ / Childhood

STEP 4
vocabulary

条件 / Condition
自然 / Nature / Natural
仮定（かてい） / Hypothetical Condition
順番（じゅんばん） / Sequential Condition
文脈（ぶんみゃく） / Contextual Condition
もし / By any chance / Supposing that
合格する（ごうかくする） / To pass
間に合う（まにあう） / To make it in time
留学する（りゅうがくする） / To study abroad
おすすめ / Recommended
絶対に（ぜったいに） / Definitely
お金持ち（おかねもち） / Rich person

STEP 5
vocabulary

接続詞（せつぞくし） / Conjunctions
追加（ついか） / Addition
主観的（しゅかんてき） / Personal / Subjective
客観的（かいかんてき） / Objective
予算（よさん） / Budget / Insufficient budget
経済（けいざい） / Economy / Growth
物価（ぶっか） / Prices (cost of living)
しかも / What's more
けれど / But / However
全体的（ぜんたいてき） / Overall
満足（まんぞく） / Satisfaction
中止（ちゅうし） / Cancellation

STEP 6
vocabulary

意図（いと） / Human Intention
準備（じゅんび） / Preparation
完了（かんりょう） / Completion
後悔（こうかい） / Regret
感情の反応（かんじょうのはんのう） / Emotional reaction
わざわざ / Going out of one's way
秘密（ひみつ） / Secret
覚える / To remember / To memorize
恥ずかしい（はずかしい） / Embarrassed
寂しい（さびしい） / Lonely
印刷する（いんさつする） / To print
受かる / To pass (an exam)

STEP 7
vocabulary

視点（してん） / Perspective
内輪（うちわ） / In-group
親切な / Kind / Helpful
行動 / Action / Behavior
さしあげる / To give (humble)
くださる / To give (honorific)
いただく / To receive (humble)
恩恵（おんけい） / Benefit / Favor
アドバイス / Advice
作文（さくぶん） / Essay
引っ越す（ひっこす） / To move
運ぶ（はこぶ） / To carry / transport

STEP 8
vocabulary

他動詞（たどうし） / Transitive verb
自動詞（じどうし） / Intransitive verb
結果 / Result / Outcome
現在 / Present time / Now
状態 / State / Condition
責任 / Responsibility
避ける（せきにんをさける） / Avoid assigning blame
文化 / Culture
割れる / To break / To crack (intransitive)
壊す / To break / To destroy (transitive)
プロジェクター / Projector
準備（じゅんび） / Ready / Prepared

STEP 9
vocabulary

外見（がいけん） / Appearance
根拠（こんきょ） / Basis
証拠（しょうこ） / Evidence / Reasoning
確実 / Certain / Certainty
移動（い移動） / Relocation
結婚（けっこん） / Marriage
連絡（れんらく） / Contact
風邪（かぜ） / Cold
雲（くも） / Cloud
噂（うわさ） / Rumor
来週 / Next week
誰か / Someone

STEP 10
vocabulary

強制（きょうせい） / Forcing someone
許可（きょか） / Permitting / Letting someone
不満（ふまん） / Dissatisfaction / Unwillingness
残業（ざんぎょう） / Overtime work
無理やり（むりやり） / Forced by someone
叱る（しかる） / To scold
上司（じょうし） / Boss
辞める / To quit / To resign
歌う / To sing
辛い / Painful / Heartbreaking (or Spicy)
教育 / Education / Training
思い出 / Memory

STEP 11
vocabulary

敬語（けいご） / Honorific Language
尊敬語（そんけいご） / Honorific (elevating others)
謙譲語（けんじょうご） / Humble (lowering yourself)
おっしゃる / To say (honorific)
召し上がる（めしあがる） / To eat/drink (honorific)
もうす / To say (humble)
伺う（うかがう） / To visit / ask (humble)
幸いです（さいわいです） / I would be grateful if ~
申し訳ございません / I am terribly sorry
かしこまりました / Understood (highly formal)
申し訳ございません / I am terribly sorry (duplicated in original)
提出する（ていしゅつする） / To submit

STEP 12
vocabulary

状況説明（じょうきょうせつめい） / Explaining situations
不可抗力（ふかこうりょく） / External pressure
〜のため / Because of ~ / Due to ~
〜により / By means of ~ / Due to ~
〜にもかかわらず / Despite ~ / In spite of ~
クッション言葉 / Transitional phrase (~te shimaimashite)
承る（うけたまわる） / To receive (humble)
ご用意（ごようい） / Preparation / Arranging (polite)
ご迷惑（ごめいわく） / Inconvenience
急遽（きゅうきょ） / Suddenly / Urgently
報告書（ほうこくしょ） / Report
解決策（かいけつさく） / Solution

STEP 13
vocabulary

論理的（ろんりてき） / Logical
説得力（せっとくりょく） / Pershesiveness / Evidence
反対意見（はんたいいけん） / Opposing view
確信度（かくしんど） / Degree of certainty
なぜなら〜だからです / This is because ~
したがって / Therefore
必要不可欠（ひつようふかけつ） / Indispensable
自己評価（じこひょうか） / Self-esteem
規制（きせい） / Regulation
創造性（そうぞうせい） / Creativity / Empathy
共存（きょうそん） / Coexist
〜ではないでしょうか / Isn't it the case that ~?
"""

def contains_kanji(text):
    return any('\u4e00' <= char <= '\u9fff' for char in text)

# Map hardcoded kana for things without furigana that contain kanji, or just use what we have.
# The user provided kana for some in parentheses.
# If there are no parentheses and there are kanji, I will use some default kana.
hardcoded_kana = {
    "何か": "なにか", "実は": "じつは", "主語": "しゅご", "条件": "じょうけん", "自然": "しぜん", "覚える": "おぼえる",
    "一番": "いちばん", "世界": "せかい", "結果": "けっか", "現在": "げんざい", "状態": "じょうたい", "責任": "せきにん", "文化": "ぶんか", "確実": "かくじつ",
    "結婚": "けっこん", "来週": "らいしゅう", "誰か": "だれか", "歌う": "うたう", "教育": "きょういく", "思い出": "おもいで", 
    "敬語": "けいご", "不可抗力": "ふかこうりょく", "クッション言葉": "くっしょんことば", "解決策": "かいけつさく", "論理的": "ろんりてき",
    "必要不可欠": "ひつようふかけつ", "自己評価": "じこひょうか", "規制": "きせい", "辞める": "やめる", "少し": "すこし", "子どものころ": "こどものころ", "漢字": "かんじ", "能力": "のうりょく", "可能性": "かのうせい", "残念": "ざんねん", "合格式": "ごうかくする", "お金持ち": "おかねもち", "追加": "ついか", "主観的": "しゅかんてき", "客観的": "きゃっかんてき", "予算": "よさん", "経済": "けいざい", "物価": "ぶっか", "全体的": "ぜんたいてき", "満足": "まんぞく", "中止": "ちゅうし", "意図": "いと", "準備": "じゅんび", "完了": "かんりょう", "後悔": "こうかい", "秘密": "ひみつ", "視点": "してん", "内輪": "うちわ", "行動": "こうどう", "恩恵": "おんけい", "作文": "さくぶん", "他動詞": "たどうし", "自動詞": "じどうし", "外見": "がいけん", "根拠": "こんきょ", "証拠": "しょうこ", "移動": "いどう", "連絡": "れんらく", "風邪": "かぜ", "雲": "くも", "噂": "うわさ", "強制": "きょうせい", "許可": "きょか", "不満": "ふまん", "残業": "ざんぎょう", "上司": "じょうし", "辛い": "つらい", "尊敬語": "そんけいご", "謙譲語": "けんじょうご", "幸いです": "さいわいです", "申し訳ございません": "もうしわけございません", "提出する": "ていしゅつする", "状況説明": "じょうきょうせつめい", "報告書": "ほうこくしょ", "説得力": "せっとくりょく", "反対意見": "はんたいいけん", "確信度": "かくしんど", "共存": "きょうぞん"
}

vocab_by_step = {}
current_step = None

for line in raw_data.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
    if line.startswith('STEP '):
        step_num = int(line.split(' ')[1])
        current_step = f"pracStep{step_num:02d}"
        vocab_by_step[current_step] = []
    elif line == 'vocabulary':
        continue
    else:
        # e.g. 新情報（しんじょうほう） / New Information
        parts = line.split(' / ')
        if len(parts) >= 2:
            jp_part = parts[0].strip()
            meaning = " / ".join(parts[1:]).strip()
            
            kanji = ""
            kana = ""
            
            # Check for parentheses for kana
            m = re.match(r'^(.*?)[（(](.*?)[)）]$', jp_part)
            if m:
                kanji = m.group(1).strip()
                kana = m.group(2).strip()
            else:
                if contains_kanji(jp_part):
                    kanji = jp_part
                    if jp_part in hardcoded_kana:
                        kana = hardcoded_kana[jp_part]
                    else:
                        kana = jp_part # Fallback, not ideal but better than empty
                else:
                    kanji = ""
                    kana = jp_part
            
            # If kanji starts with 〜, keep it
            
            vocab_by_step[current_step].append({
                "kana": kana,
                "kanji": kanji,
                "romaji": "",
                "meaning": meaning
            })

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

def replace_vocab(m):
    step_id = m.group(1)
    if step_id in vocab_by_step:
        # Remove duplicates like 申し訳ございません in STEP 11
        unique_vocab = []
        seen = set()
        for item in vocab_by_step[step_id]:
            key = item['kanji'] + item['kana']
            if key not in seen:
                seen.add(key)
                unique_vocab.append(item)
        
        vocab_str = json.dumps(unique_vocab, ensure_ascii=False)
        # The regex captured: (pracStepXX): ({"title": "...", "videoUrl": "", )"vocabulary": \[.*?\]
        return f'{step_id}: {m.group(2)}"vocabulary": {vocab_str}'
    return m.group(0)

new_text = re.sub(r'(pracStep\d{2}): (\{.*?"videoUrl"\s*:\s*".*?"\s*,\s*)"vocabulary"\s*:\s*\[.*?\]', replace_vocab, text, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Updated index.html!")
