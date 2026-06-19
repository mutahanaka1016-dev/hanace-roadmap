import re

good_vocab = {
    # Beginner / Intermediate Verbs
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

    # Advanced chunks and phrases
    "<ruby>選<rt>えら</rt></ruby>びました": "[V] Chose",
    "<ruby>食<rt>た</rt></ruby>べません": "[V] Do not eat",
    "<ruby>思<rt>おも</rt></ruby>います": "[V] Think",
    "みつかりました": "[V] Was found",
    "ありました": "[V] Was / Existed",
    "おいしくない": "[Adj] Not delicious",
    "<ruby>頭<rt>あたま</rt></ruby>がいい": "[Adj] Smart",
    "<ruby>勉強<rt>べんきょう</rt></ruby>すれば": "[Phrase] If you study",
    "するほど": "[Phrase] The more you do",
    "<ruby>上手<rt>じょうず</rt></ruby>になります": "[Phrase] Become good at",
    "<ruby>怠<rt>なま</rt></ruby>ける": "[V] To slack off",
    "<ruby>話<rt>はな</rt></ruby>す": "[V] To speak",
    "<ruby>弾<rt>ひ</rt></ruby>けます": "[V] Can play",
    "<ruby>行<rt>い</rt></ruby>く<ruby>前<rt>まえ</rt></ruby>": "[Phrase] Before going",
    "<ruby>話<rt>はな</rt></ruby>せませんでした": "[V] Could not speak",
    "<ruby>食<rt>た</rt></ruby>べられます": "[V] Can eat",
    "<ruby>回<rt>まわ</rt></ruby>ると": "[Phrase] If you turn",
    "<ruby>旅行<rt>りょこう</rt></ruby>したい": "[Phrase] Want to travel",
    "<ruby>行<rt>い</rt></ruby>くなら": "[Phrase] If you go",
    "<ruby>絶対<rt>ぜったい</rt></ruby>に<ruby>行<rt>い</rt></ruby>": "[Adv] Definitely go",
    "<ruby>行<rt>い</rt></ruby>ったほうがいい": "[Phrase] Should go",
    "<ruby>書<rt>か</rt></ruby>けば": "[Phrase] If you write",
    "うまくなります": "[Phrase] Will become good",
    "<ruby>遅<rt>おく</rt></ruby>れました": "[V] Was late",
    "<ruby>遅刻<rt>ちこく</rt></ruby>しました": "[V] Was late",
    "<ruby>足<rt>た</rt></ruby>りません": "[V] Is not enough",
    "<ruby>近<rt>ちか</rt></ruby>い": "[Adj] Near",
    "<ruby>安<rt>やす</rt></ruby>い": "[Adj] Cheap",
    "<ruby>楽<rt>たの</rt></ruby>しい": "[Adj] Fun",
    "<ruby>欠<rt>か</rt></ruby>かしません": "[V] Do not miss",
    "<ruby>来<rt>き</rt></ruby>てくださって": "[Phrase] Thank you for coming",
    "あけてある": "[Phrase] Is left open",
    "<ruby>予約<rt>よやく</rt></ruby>しておきました": "[Phrase] Made a reservation in advance",
    "<ruby>食<rt>た</rt></ruby>べてしまいました": "[Phrase] Ate completely",
    "くれました": "[V] Gave to me",
    "もらいました": "[V] Received",
    "いただきました": "[V] Received (humble)",
    "<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>す": "[V] To move",
    "<ruby>手伝<rt>てつだ</rt></ruby>ってもらえますか": "[Phrase] Can you help me",
    "<ruby>壊<rt>こわ</rt></ruby>れました": "[V] Broke (intransitive)",
    "<ruby>壊<rt>こわ</rt></ruby>しました": "[V] Broke (transitive)",
    "<ruby>開<rt>あ</rt></ruby>けてあります": "[Phrase] Is left open",
    "<ruby>開<rt>あ</rt></ruby>いています": "[Phrase] Is open",
    "<ruby>降<rt>ふ</rt></ruby>りそうです": "[Phrase] Looks like it will rain",
    "<ruby>移動<rt>いどう</rt></ruby>するそうです": "[Phrase] I heard will move",
    "<ruby>結婚<rt>けっこん</rt></ruby>するらしい": "[Phrase] Seems will marry",
    "<ruby>連絡<rt>れんらく</rt></ruby>した": "[V] Contacted",
    "つながらなくて": "[Phrase] Couldn't connect",
    "ひいたみたい": "[Phrase] Looks like caught (a cold)",
    "<ruby>食<rt>た</rt></ruby>べられました": "[V] Was eaten",
    "<ruby>考<rt>かんが</rt></ruby>えさせて": "[Phrase] Let me think",
    "<ruby>練習<rt>れんしゅう</rt></ruby>させられました": "[Phrase] Was made to practice",
    "<ruby>言<rt>い</rt></ruby>われてしまいました": "[Phrase] Was told regretfully",
    "おもちいたします": "[Phrase] Will carry (humble)",
    "おうかがいしてもよろしいでしょうか": "[Phrase] May I ask (humble)",
    "お<ruby>世話<rt>せわ</rt></ruby>になっております": "[Phrase] Indebted / Thank you for your support",
    "<ruby>提出<rt>ていしゅつ</rt></ruby>していただけますか": "[Phrase] Could you submit",
    "<ruby>壊<rt>こわ</rt></ruby>れてしまいまして": "[Phrase] Broke regretfully",
    "<ruby>残業<rt>ざんぎょう</rt></ruby>させられた": "[Phrase] Was made to work overtime",
    "<ruby>遅<rt>おく</rt></ruby>れてしまいました": "[Phrase] Was late regretfully",
    "とっておきました": "[Phrase] Kept in advance",
    "<ruby>発達<rt>はったつ</rt></ruby>すれば": "[Phrase] If develop",
    "<ruby>減<rt>へ</rt></ruby>っていく": "[Phrase] Will decrease",
    "<ruby>考<rt>かん</rt></ruby>がえます": "[V] Think",
    "<ruby>話<rt>はな</rt></ruby>せるならば": "[Phrase] If can speak",
    "<ruby>与<rt>あた</rt></ruby>える": "[V] To give",
    "<ruby>比<rt>くら</rt></ruby>べると": "[Phrase] Compared to",
    "<ruby>発達<rt>はったつ</rt></ruby>している": "[Phrase] Is developed",
    
    # Ensuring "ください" or other parts don't get isolated
    "<ruby>考<rt>かんが</rt></ruby>えさせてください": "[Phrase] Please let me think",
    "手伝って": "[V] To help (te-form)",
    "<ruby>運<rt>はこ</rt></ruby>んで": "[V] To carry (te-form)",
    "<ruby>提出<rt>ていしゅつ</rt></ruby>いたします": "[Phrase] Will submit (humble)",
    "<ruby>取<rt>と</rt></ruby>りかからせられて": "[Phrase] Was forced to start",
}

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

entries_js = ""
for k, v in good_vocab.items():
    entries_js += f'            "{k}": "{v}",\n'

pattern_global = r"(const GLOBAL_VOCAB = \{)"

def repl(m):
    return m.group(1) + "\n" + entries_js

new_text, count = re.subn(pattern_global, repl, text, count=1)
if count > 0:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Successfully restored perfectly formed verbs/phrases to GLOBAL_VOCAB.")
else:
    print("Failed to find GLOBAL_VOCAB.")
