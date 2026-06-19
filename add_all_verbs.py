import re

new_verbs = {
    "<ruby>行<rt>い</rt></ruby>きます": "[V] Go",
    "<ruby>行<rt>い</rt></ruby>きました": "[V] Went",
    "<ruby>行<rt>い</rt></ruby>ってみたいと": "[V] Want to try going",
    "<ruby>行<rt>い</rt></ruby>くつもりです": "[V] Intend to go",
    "<ruby>行<rt>い</rt></ruby>ったことがあります": "[V] Have been to",
    "<ruby>行<rt>い</rt></ruby>かなきゃ": "[V] Must go",
    "<ruby>見<rt>み</rt></ruby>ます": "[V] Watch / See",
    "<ruby>見<rt>み</rt></ruby>ました": "[V] Watched / Saw",
    "<ruby>見<rt>み</rt></ruby>たことがあります": "[V] Have seen",
    "<ruby>見<rt>み</rt></ruby>ることです": "[V] To watch",
    "<ruby>食<rt>た</rt></ruby>べます": "[V] Eat",
    "<ruby>食<rt>た</rt></ruby>べました": "[V] Ate",
    "<ruby>食<rt>た</rt></ruby>べないで": "[V] Without eating",
    "<ruby>食<rt>た</rt></ruby>べたことがあります": "[V] Have eaten",
    "<ruby>食<rt>た</rt></ruby>べたことがありません": "[V] Have not eaten",
    "<ruby>食<rt>た</rt></ruby>べませんか": "[V] Won't you eat?",
    "<ruby>飲<rt>の</rt></ruby>みません": "[V] Do not drink",
    "<ruby>休<rt>やす</rt></ruby>みます": "[V] Rest / Take a day off",
    "<ruby>浴<rt>あび</rt></ruby>て": "[V] Bathe (te-form)",
    "<ruby>話<rt>はな</rt></ruby>してください": "[V] Please speak",
    "<ruby>住<rt>す</rt></ruby>んでいます": "[V] Living",
    "<ruby>出<rt>だ</rt></ruby>さなければならない": "[V] Must submit / Must turn in",
    "<ruby>寝<rt>ね</rt></ruby>ないで": "[V] Without sleeping",
    "<ruby>寝<rt>ね</rt></ruby>ます": "[V] Sleep",
    "<ruby>降<rt>ふ</rt></ruby>ると": "[V] Fall (rain, snow)",
    "<ruby>降<rt>ふ</rt></ruby>っているから": "[V] Because it is raining",
    "<ruby>言<rt>い</rt></ruby>っていました": "[V] Was saying",
    "<ruby>言<rt>い</rt></ruby>っていたので": "[V] Because they said",
    "<ruby>手伝<rt>てつだ</rt></ruby>ってほしいです": "[V] Want you to help",
    "<ruby>治<rt>なお</rt></ruby>ってほしいです": "[V] Want it to heal / recover",
    "<ruby>作<rt>つく</rt></ruby>ることが": "[V] Making (cooking)",
    "<ruby>弾<rt>ひ</rt></ruby>きます": "[V] Play (instrument)",
    "<ruby>始<rt>はじ</rt></ruby>めました": "[V] Started",
    "<ruby>出<rt>で</rt></ruby>かけます": "[V] Go out",
    "<ruby>決<rt>き</rt></ruby>めていません": "[V] Have not decided",
    "あります": "[V] Is / Exist / Have (inanimate)",
    "います": "[V] Is / Exist (animate)",
    "ひいたので": "[V] Because I caught (a cold)",
    "します": "[V] Do",
    "しました": "[V] Did",
    "しています": "[V] Am doing / Have been doing",
    "できませんでした": "[V] Could not do",
    "あげました": "[V] Gave"
}

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

entries_js = ""
for k, v in new_verbs.items():
    entries_js += f'            "{k}": "{v}",\n'

pattern = r"(const GLOBAL_VOCAB = \{)"

def repl(m):
    return m.group(1) + "\n" + entries_js

new_content, count = re.subn(pattern, repl, content, count=1)
if count > 0:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Successfully injected {len(new_verbs)} verbs into GLOBAL_VOCAB.")
else:
    print("Failed to find GLOBAL_VOCAB.")
