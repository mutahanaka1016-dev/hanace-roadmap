import re
import json

# Target chunks and their meanings that we want to ensure match perfectly with ruby tags
target_chunks = {
    "選びました": "[V] Chose",
    "食べます": "[V] Eat",
    "食べません": "[V] Do not eat",
    "思います": "[V] Think",
    "みつかりました": "[V] Was found",
    "ありました": "[V] Was / Existed",
    "おいしくない": "[Adj] Not delicious",
    "頭がいい": "[Adj] Smart",
    "勉強すれば": "[Phrase] If you study",
    "するほど": "[Phrase] The more you do",
    "上手になります": "[Phrase] Become good at",
    "怠ける": "[V] To slack off",
    "話す": "[V] To speak",
    "弾けます": "[V] Can play",
    "行く前": "[Phrase] Before going",
    "話せませんでした": "[V] Could not speak",
    "食べられます": "[V] Can eat",
    "回ると": "[Phrase] If you turn",
    "旅行したい": "[Phrase] Want to travel",
    "行くなら": "[Phrase] If you go",
    "絶対に行": "[Adv] Definitely go",
    "行ったほうがいい": "[Phrase] Should go",
    "書けば": "[Phrase] If you write",
    "うまくなります": "[Phrase] Will become good",
    "遅れました": "[V] Was late",
    "遅刻しました": "[V] Was late",
    "足りません": "[V] Is not enough",
    "近い": "[Adj] Near",
    "安い": "[Adj] Cheap",
    "楽しい": "[Adj] Fun",
    "欠かしません": "[V] Do not miss",
    "来てくださって": "[Phrase] Thank you for coming",
    "あけてある": "[Phrase] Is left open",
    "予約しておきました": "[Phrase] Made a reservation in advance",
    "食べてしまいました": "[Phrase] Ate completely",
    "くれました": "[V] Gave to me",
    "もらいました": "[V] Received",
    "いただきました": "[V] Received (humble)",
    "引っ越す": "[V] To move",
    "手伝ってもらえますか": "[Phrase] Can you help me",
    "壊れました": "[V] Broke (intransitive)",
    "壊しました": "[V] Broke (transitive)",
    "開けてあります": "[Phrase] Is left open",
    "開いています": "[Phrase] Is open",
    "降りそうです": "[Phrase] Looks like it will rain",
    "移動するそうです": "[Phrase] I heard will move",
    "結婚するらしい": "[Phrase] Seems will marry",
    "連絡した": "[V] Contacted",
    "つながらなくて": "[Phrase] Couldn't connect",
    "ひいたみたい": "[Phrase] Looks like caught (a cold)",
    "食べられました": "[V] Was eaten",
    "考えさせて": "[Phrase] Let me think",
    "練習させられました": "[Phrase] Was made to practice",
    "言われてしまいました": "[Phrase] Was told regretfully",
    "おもちいたします": "[Phrase] Will carry (humble)",
    "おうかがいしてもよろしいでしょうか": "[Phrase] May I ask (humble)",
    "お世話になっております": "[Phrase] Indebted / Thank you for your support",
    "提出していただけますか": "[Phrase] Could you submit",
    "壊れてしまいまして": "[Phrase] Broke regretfully",
    "残業させられた": "[Phrase] Was made to work overtime",
    "遅れてしまいました": "[Phrase] Was late regretfully",
    "とっておきました": "[Phrase] Kept in advance",
    "発達すれば": "[Phrase] If develop",
    "減っていく": "[Phrase] Will decrease",
    "考えます": "[V] Think",
    "話せるならば": "[Phrase] If can speak",
    "与える": "[V] To give",
    "比べると": "[Phrase] Compared to",
    "発達している": "[Phrase] Is developed",
    
    # Verbs from Beginner/Intermediate steps just in case
    "行きます": "[V] Go",
    "行きました": "[V] Went",
    "行ってみたいと": "[V] Want to try going",
    "行くつもりです": "[V] Intend to go",
    "行ったことがあります": "[V] Have been to",
    "行かなきゃ": "[V] Must go",
    "見ます": "[V] Watch / See",
    "見ました": "[V] Watched / Saw",
    "見たことがあります": "[V] Have seen",
    "見ることです": "[V] To watch",
    "食べないで": "[V] Without eating",
    "食べたことがあります": "[V] Have eaten",
    "食べたことがありません": "[V] Have not eaten",
    "食べませんか": "[V] Won't you eat?",
    "飲みません": "[V] Do not drink",
    "休みます": "[V] Rest / Take a day off",
    "浴びて": "[V] Bathe (te-form)",
    "話してください": "[V] Please speak",
    "住んでいます": "[V] Living",
    "出さなければならない": "[V] Must submit / Must turn in",
    "寝ないで": "[V] Without sleeping",
    "寝ます": "[V] Sleep",
    "降ると": "[V] Fall (rain, snow)",
    "降っているから": "[V] Because it is raining",
    "言っていました": "[V] Was saying",
    "言っていたので": "[V] Because they said",
    "手伝ってほしいです": "[V] Want you to help",
    "治ってほしいです": "[V] Want it to heal / recover",
    "作ることが": "[V] Making (cooking)",
    "始めました": "[V] Started",
    "出かけます": "[V] Go out",
    "決めていません": "[V] Have not decided",
    "ひいたので": "[V] Because I caught (a cold)",
    "できませんでした": "[V] Could not do",
    "あげました": "[V] Gave",
    
    # Nouns and Adjectives
    "映画": "[N] Movie",
    "刺身": "[N] Sashimi",
    "日本語": "[N] Japanese",
    "難しい": "[Adj] Difficult",
    "財布": "[N] Wallet",
    "交番": "[N] Police box",
    "東京": "[N] Tokyo",
    "大阪": "[N] Osaka",
    "食べ物": "[N] Food",
    "クラス": "[N] Class",
    "田中": "[N] Tanaka",
    "勉強": "[N] Study",
    "便利": "[Adj] Convenient",
    "人間": "[N] Human",
    "ピアノ": "[N] Piano",
    "日本": "[N] Japan",
    "なっとう": "[N] Natto",
    "右": "[N] Right",
    "郵便局": "[N] Post office",
    "お金": "[N] Money",
    "旅行": "[N] Travel",
    "京都": "[N] Kyoto",
    "絶対に": "[Adv] Definitely",
    "毎日": "[Adv] Every day",
    "日記": "[N] Diary",
    "電車": "[N] Train",
    "会議": "[N] Meeting",
    "計画": "[N] Plan",
    "予算": "[N] Budget",
    "アパート": "[N] Apartment",
    "練習": "[N] Practice",
    "わざわざ": "[Adv] Taking the trouble",
    "窓": "[N] Window",
    "ホテル": "[N] Hotel",
    "全部": "[Adv] All",
    "先生": "[N] Teacher",
    "アドバイス": "[N] Advice",
    "今度": "[N] Next time",
    "おもちゃ": "[N] Toy",
    "雨": "[N] Rain",
    "来年": "[N] Next year",
    "会社": "[N] Company",
    "彼女": "[N] She",
    "来週": "[N] Next week",
    "携帯": "[N] Mobile phone",
    "風邪": "[N] Cold",
    "友達": "[N] Friend",
    "ケーキ": "[N] Cake",
    "少し": "[Adv] A little",
    "子ども": "[N] Child",
    "上司": "[N] Boss",
    "ひどいこと": "[N] Terrible thing",
    "名前": "[N] Name",
    "レポート": "[N] Report",
    "機械": "[N] Machine",
    "連絡": "[N] Contact",
    "予約": "[N] Reservation",
    "バックアップ": "[N] Backup",
    "テクノロジー": "[N] Technology",
    "仕事": "[N] Work",
    "世界中": "[N] All over the world",
    "文化交流": "[N] Cultural exchange",
    "盛ん": "[Adj] Active / Prosperous",
    "若者": "[N] Young people",
    "悪い": "[Adj] Bad",
    "影響": "[N] Influence",
    "国": "[N] Country",
    "公共交通": "[N] Public transportation"
}

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find all jp fields to scan. Account for {"jp": "..."} AND {jp: '...'}
pattern = r"['\"]?jp['\"]?\s*:\s*['\"](.*?)['\"]"
jps = re.findall(pattern, text)

ruby_tagged_vocab = {}

def get_ruby_mapping(html_str):
    # Returns (plain_text, mapping_from_plain_idx_to_html_idx)
    plain = []
    mapping = []
    i = 0
    in_rt = False
    in_tag = False
    html_i = 0
    while html_i < len(html_str):
        if html_str[html_i:html_i+4] == "<rt>":
            in_rt = True
            html_i += 4
            continue
        if html_str[html_i:html_i+5] == "</rt>":
            in_rt = False
            html_i += 5
            continue
            
        if html_str[html_i] == "<":
            in_tag = True
        
        if not in_rt and not in_tag:
            plain.append(html_str[html_i])
            mapping.append(html_i)
            
        if html_str[html_i] == ">":
            in_tag = False
            
        html_i += 1
    
    mapping.append(html_i)
    return "".join(plain), mapping

for jp in jps:
    plain, mapping = get_ruby_mapping(jp)
    for raw_verb, meaning in target_chunks.items():
        if raw_verb in plain:
            idx = 0
            while True:
                idx = plain.find(raw_verb, idx)
                if idx == -1:
                    break
                
                html_start = mapping[idx]
                html_end = mapping[idx + len(raw_verb)]
                
                end_cursor = html_end
                while jp[end_cursor:end_cursor+7] == "</ruby>":
                    end_cursor += 7
                
                start_cursor = html_start
                while jp[start_cursor-6:start_cursor] == "<ruby>":
                    start_cursor -= 6
                
                exact_html = jp[start_cursor:end_cursor]
                ruby_tagged_vocab[exact_html] = meaning
                idx += 1

print(f"Extracted {len(ruby_tagged_vocab)} ruby-tagged entries.")

entries_js = ""
for k, v in ruby_tagged_vocab.items():
    entries_js += f'            "{k}": "{v}",\n'

pattern_global = r"(const GLOBAL_VOCAB = \{)"

def repl(m):
    return m.group(1) + "\n" + entries_js

new_text, count = re.subn(pattern_global, repl, text, count=1)
if count > 0:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Successfully injected completely correct ruby-tagged vocabulary into GLOBAL_VOCAB.")
else:
    print("Failed to find GLOBAL_VOCAB.")
