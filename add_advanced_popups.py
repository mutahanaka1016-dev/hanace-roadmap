import re

new_entries = {
    "映画": "[N] Movie",
    "私": "[Pron.] I / Me",
    "選びました": "[V] Chose",
    "刺身": "[N] Sashimi",
    "食べます": "[V] Eat",
    "肉": "[N] Meat",
    "食べません": "[V] Do not eat",
    "日本語": "[N] Japanese",
    "難しい": "[Adj] Difficult",
    "思います": "[V] Think",
    "実は": "[Adv] Actually / To tell the truth",
    "財布": "[N] Wallet",
    "みつかりました": "[V] Was found",
    "駅": "[N] Station",
    "交番": "[N] Police box",
    "ありました": "[V] Was / Existed",

    "東京": "[N] Tokyo",
    "大阪": "[N] Osaka",
    "食べ物": "[N] Food",
    "おいしくない": "[Adj] Not delicious",
    "クラス": "[N] Class",
    "田中": "[N] Tanaka",
    "頭がいい": "[Adj] Smart",
    "勉強": "[N] Study",
    "勉強すれば": "[Phrase] If you study",
    "するほど": "[Phrase] The more you do",
    "上手になります": "[Phrase] Become good at",
    "便利": "[Adj] Convenient",
    "人間": "[N] Human",
    "怠ける": "[V] To slack off",

    "話す": "[V] To speak",
    "ピアノ": "[N] Piano",
    "弾けます": "[V] Can play",
    "日本": "[N] Japan",
    "行く前": "[Phrase] Before going",
    "話せませんでした": "[V] Could not speak",
    "なっとう": "[N] Natto",
    "食べられます": "[V] Can eat",

    "右": "[N] Right",
    "回ると": "[Phrase] If you turn",
    "郵便局": "[N] Post office",
    "お金": "[N] Money",
    "旅行したい": "[Phrase] Want to travel",
    "行くなら": "[Phrase] If you go",
    "京都": "[N] Kyoto",
    "絶対に": "[Adv] Definitely",
    "行ったほうがいい": "[Phrase] Should go",
    "毎日": "[Adv] Every day",
    "日記": "[N] Diary",
    "書けば": "[Phrase] If you write",
    "うまくなります": "[Phrase] Will become good",

    "電車": "[N] Train",
    "遅れました": "[V] Was late",
    "会議": "[N] Meeting",
    "遅刻しました": "[V] Was late",
    "計画": "[N] Plan",
    "予算": "[N] Budget",
    "足りません": "[V] Is not enough",
    "アパート": "[N] Apartment",
    "近い": "[Adj] Near",
    "安い": "[Adj] Cheap",
    "楽しい": "[Adj] Fun",
    "練習": "[N] Practice",
    "欠かしません": "[V] Do not miss",

    "わざわざ": "[Adv] Taking the trouble",
    "来てくださって": "[Phrase] Thank you for coming",
    "窓": "[N] Window",
    "あけてある": "[Phrase] Is left open",
    "旅行": "[N] Travel",
    "ホテル": "[N] Hotel",
    "予約しておきました": "[Phrase] Made a reservation in advance",
    "全部": "[Adv] All",
    "食べてしまいました": "[Phrase] Ate completely",

    "先生": "[N] Teacher",
    "アドバイス": "[N] Advice",
    "くれました": "[V] Gave to me",
    "もらいました": "[V] Received",
    "いただきました": "[V] Received (humble)",
    "今度": "[N] Next time",
    "引っ越す": "[V] To move",
    "手伝ってもらえますか": "[Phrase] Can you help me",

    "おもちゃ": "[N] Toy",
    "壊れました": "[V] Broke (intransitive)",
    "壊しました": "[V] Broke (transitive)",
    "開けてあります": "[Phrase] Is left open",
    "開いています": "[Phrase] Is open",

    "雨": "[N] Rain",
    "降りそうです": "[Phrase] Looks like it will rain",
    "来年": "[N] Next year",
    "会社": "[N] Company",
    "移動するそうです": "[Phrase] I heard will move",
    "彼女": "[N] She",
    "来週": "[N] Next week",
    "結婚するらしい": "[Phrase] Seems will marry",
    "携帯": "[N] Mobile phone",
    "連絡した": "[V] Contacted",
    "つながらなくて": "[Phrase] Couldn't connect",
    "風邪": "[N] Cold",
    "ひいたみたい": "[Phrase] Looks like caught (a cold)",

    "友達": "[N] Friend",
    "ケーキ": "[N] Cake",
    "食べられました": "[V] Was eaten",
    "少し": "[Adv] A little",
    "考えさせて": "[Phrase] Let me think",
    "子ども": "[N] Child",
    "練習させられました": "[Phrase] Was made to practice",
    "上司": "[N] Boss",
    "ひどいこと": "[N] Terrible thing",
    "言われてしまいました": "[Phrase] Was told regretfully",

    "おもちいたします": "[Phrase] Will carry (humble)",
    "名前": "[N] Name",
    "おうかがいしてもよろしいでしょうか": "[Phrase] May I ask (humble)",
    "お世話になっております": "[Phrase] Indebted / Thank you for your support",
    "レポート": "[N] Report",
    "提出していただけますか": "[Phrase] Could you submit",

    "機械": "[N] Machine",
    "壊れてしまいまして": "[Phrase] Broke regretfully",
    "残業させられた": "[Phrase] Was made to work overtime",
    "連絡": "[N] Contact",
    "遅れてしまいました": "[Phrase] Was late regretfully",
    "予約": "[N] Reservation",
    "バックアップ": "[N] Backup",
    "とっておきました": "[Phrase] Kept in advance",

    "テクノロジー": "[N] Technology",
    "発達すれば": "[Phrase] If develop",
    "仕事": "[N] Work",
    "減っていく": "[Phrase] Will decrease",
    "考えます": "[V] Think",
    "世界中": "[N] All over the world",
    "話せるならば": "[Phrase] If can speak",
    "文化交流": "[N] Cultural exchange",
    "盛ん": "[Adj] Active / Prosperous",
    "若者": "[N] Young people",
    "悪い": "[Adj] Bad",
    "影響": "[N] Influence",
    "与える": "[V] To give",
    "国": "[N] Country",
    "比べると": "[Phrase] Compared to",
    "公共交通": "[N] Public transportation",
    "発達している": "[Phrase] Is developed",
    "思います": "[V] Think"
}

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Generate the javascript entries
entries_js = ""
for k, v in new_entries.items():
    entries_js += f'            "{k}": "{v}",\n'

# Find GLOBAL_VOCAB
# Replace "const GLOBAL_VOCAB = {" with "const GLOBAL_VOCAB = {\n" + entries_js
pattern = r"(const GLOBAL_VOCAB = \{)"

def repl(m):
    return m.group(1) + "\n" + entries_js

new_content, count = re.subn(pattern, repl, content, count=1)
if count > 0:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully injected advanced vocabulary into GLOBAL_VOCAB.")
else:
    print("Failed to find GLOBAL_VOCAB.")
