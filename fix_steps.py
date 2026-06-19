import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# First, find the first pracStep13 and replace it with pracStep07
# The first pracStep13 is right after pracStep02.
# We will use regex to find pracStep13 block that is followed by pracStep03

pattern = r"pracStep13:\s*\{.*?\"quizzes\":\s*\[\]\},(\s*pracStep03:)"

prac_step_07 = '''pracStep07: {"title": "Giving & Receiving", "videoUrl": "", "vocabulary": [{"kana": "じゅじゅひょうげん", "kanji": "授受表現", "romaji": "", "meaning": "Giving & Receiving expressions"}, {"kana": "してん", "kanji": "視点", "romaji": "", "meaning": "Perspective"}, {"kana": "うちわ", "kanji": "内輪", "romaji": "", "meaning": "In-group"}, {"kana": "しんせつなこうどう", "kanji": "親切な行動", "romaji": "", "meaning": "Kind action"}, {"kana": "さしあげる", "kanji": "", "romaji": "", "meaning": "To give (humble)"}, {"kana": "くださる", "kanji": "", "romaji": "", "meaning": "To give (honorific)"}, {"kana": "いただく", "kanji": "", "romaji": "", "meaning": "To receive (humble)"}, {"kana": "おんけい", "kanji": "恩恵", "romaji": "", "meaning": "Benefit"}, {"kana": "アドバイス", "kanji": "", "romaji": "", "meaning": "Advice"}, {"kana": "さくぶん", "kanji": "作文", "romaji": "", "meaning": "Essay"}, {"kana": "ひっこす", "kanji": "引っ越す", "romaji": "", "meaning": "To move"}, {"kana": "はこぶ", "kanji": "運ぶ", "romaji": "", "meaning": "To carry"}], "examples": [{"jp": "<ruby>先生<rt>せんせい</rt></ruby>は<ruby>私<rt>わたし</rt></ruby>にアドバイスをくれました。", "romaji": "", "en": ""}, {"jp": "<ruby>私<rt>わたし</rt></ruby>は<ruby>先生<rt>せんせい</rt></ruby>にアドバイスをもらいました。", "romaji": "", "en": ""}, {"jp": "<ruby>先生<rt>せんせい</rt></ruby>にアドバイスをいただきました。", "romaji": "", "en": ""}, {"jp": "<ruby>今度<rt>こんど</rt></ruby>、<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>すんですが、<ruby>手伝<rt>てつだ</rt></ruby>ってもらえますか？", "romaji": "", "en": ""}], "quizzes": []},'''

def repl(m):
    return prac_step_07 + m.group(1)

new_text = re.sub(pattern, repl, text, count=1, flags=re.DOTALL)

# But wait, pracStep07 should be placed before pracStep08!
# If I replace the first pracStep13 with pracStep07, pracStep07 will be before pracStep03!
# This is wrong order!
# The correct order is 01, 02, 03, 04, 05, 06, 07, 08...
# Let's just remove the first pracStep13 completely.
new_text = re.sub(pattern, r"\1", text, count=1, flags=re.DOTALL)

# Now, insert pracStep07 before pracStep08
pattern2 = r"(\s*pracStep08:)"
new_text = re.sub(pattern2, r"\n            " + prac_step_07 + r"\1", new_text, count=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Fixed steps")
