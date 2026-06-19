import re
import json

new_examples = {
    1: [
        "この<ruby>映画<rt>えいが</rt></ruby>は<ruby>私<rt>わたし</rt></ruby>が<ruby>選<rt>えら</rt></ruby>びました。",
        "<ruby>刺身<rt>さしみ</rt></ruby>は<ruby>食<rt>た</rt></ruby>べます。<ruby>肉<rt>にく</rt></ruby>は<ruby>食<rt>た</rt></ruby>べません。",
        "<ruby>私<rt>わたし</rt></ruby>は<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>難<rt>むずか</rt></ruby>しいと<ruby>思<rt>おも</rt></ruby>います。",
        "<ruby>実<rt>じつ</rt></ruby>は、<ruby>財布<rt>さいふ</rt></ruby>がみつかりました！<ruby>財布<rt>さいふ</rt></ruby>は<ruby>駅<rt>えき</rt></ruby>の<ruby>交番<rt>こうばん</rt></ruby>にありました。"
    ],
    2: [
        "<ruby>東京<rt>とうきょう</rt></ruby>は<ruby>大阪<rt>おおさか</rt></ruby>ほど<ruby>食<rt>た</rt></ruby>べ<ruby>物<rt>もの</rt></ruby>がおいしくない。",
        "このクラスのなかで、<ruby>田中<rt>たなか</rt></ruby>さんがいちばん<ruby>頭<rt>あたま</rt></ruby>がいいです。",
        "<ruby>勉強<rt>べんきょう</rt></ruby>すればするほど、<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>上手<rt>じょうず</rt></ruby>になります。",
        "<ruby>便利<rt>べんり</rt></ruby>になればなるほど、<ruby>人間<rt>にんげん</rt></ruby>は<ruby>怠<rt>なま</rt></ruby>けるようになります。"
    ],
    3: [
        "<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>話<rt>はな</rt></ruby>すことができます。",
        "ピアノが<ruby>弾<rt>ひ</rt></ruby>けます",
        "<ruby>日本<rt>にほん</rt></ruby>に<ruby>行<rt>い</rt></ruby>く<ruby>前<rt>まえ</rt></ruby>は、<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>話<rt>はな</rt></ruby>せませんでした。",
        "なっとうが<ruby>食<rt>た</rt></ruby>べられますか？"
    ],
    4: [
        "<ruby>右<rt>みぎ</rt></ruby>に<ruby>回<rt>まわ</rt></ruby>ると、<ruby>郵便局<rt>ゆうびんきょく</rt></ruby>があります。",
        "お<ruby>金<rt>かね</rt></ruby>があれば、<ruby>旅行<rt>りょこう</rt></ruby>したいです。",
        "<ruby>日本<rt>にほん</rt></ruby>に<ruby>行<rt>い</rt></ruby>くなら、<ruby>京都<rt>きょうと</rt></ruby>は<ruby>絶対<rt>ぜったい</rt></ruby>に<ruby>行<rt>い</rt></ruby>ったほうがいいですよ。",
        "<ruby>毎日<rt>まいにち</rt></ruby><ruby>日本語<rt>にほんご</rt></ruby>で<ruby>日記<rt>にっき</rt></ruby>を<ruby>書<rt>か</rt></ruby>けば、<ruby>絶対<rt>ぜったい</rt></ruby>にうまくなりますよ！"
    ],
    5: [
        "<ruby>電車<rt>でんしゃ</rt></ruby>が<ruby>遅<rt>おく</rt></ruby>れました。それで、<ruby>会議<rt>かいぎ</rt></ruby>に<ruby>遅刻<rt>ちこく</rt></ruby>しました。",
        "この<ruby>計画<rt>けいかく</rt></ruby>はいいと<ruby>思<rt>おも</rt></ruby>います。けれど、<ruby>予算<rt>よさん</rt></ruby>が<ruby>足<rt>た</rt></ruby>りません。",
        "このアパートは<ruby>駅<rt>えき</rt></ruby>に<ruby>近<rt>ちか</rt></ruby>いです。しかも、<ruby>安<rt>やす</rt></ruby>いです！",
        "<ruby>日本語<rt>にほんご</rt></ruby>は<ruby>難<rt>むずか</rt></ruby>しいです。けれど、とても<ruby>楽<rt>たの</rt></ruby>しいです。さらに、<ruby>勉強<rt>べんきょう</rt></ruby>すればするほど、<ruby>上手<rt>じょうず</rt></ruby>になります。だから、<ruby>毎日<rt>まいにち</rt></ruby><ruby>練習<rt>れんしゅう</rt></ruby>を<ruby>欠<rt>か</rt></ruby>かしません。"
    ],
    6: [
        "わざわざ<ruby>来<rt>き</rt></ruby>てくださってありがとうございます。",
        "<ruby>窓<rt>まど</rt></ruby>があけてある。",
        "<ruby>旅行<rt>りょこう</rt></ruby>の<ruby>前<rt>まえ</rt></ruby>に、ホテルを<ruby>予約<rt>よやく</rt></ruby>しておきました。",
        "ケーキを<ruby>全部<rt>ぜんぶ</rt></ruby><ruby>食<rt>た</rt></ruby>べてしまいました。"
    ],
    7: [
        "<ruby>先生<rt>せんせい</rt></ruby>は<ruby>私<rt>わたし</rt></ruby>にアドバイスをくれました。",
        "<ruby>私<rt>わたし</rt></ruby>は<ruby>先生<rt>せんせい</rt></ruby>にアドバイスをもらいました。",
        "<ruby>先生<rt>せんせい</rt></ruby>にアドバイスをいただきました。",
        "<ruby>今度<rt>こんど</rt></ruby>、<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>すんですが、<ruby>手伝<rt>てつだ</rt></ruby>ってもらえますか？"
    ],
    8: [
        "おもちゃが<ruby>壊<rt>こわ</rt></ruby>れました。",
        "おもちゃを<ruby>壊<rt>こわ</rt></ruby>しました。",
        "<ruby>窓<rt>まど</rt></ruby>が<ruby>開<rt>あ</rt></ruby>けてあります。",
        "<ruby>窓<rt>まど</rt></ruby>が<ruby>開<rt>あ</rt></ruby>いています。"
    ],
    9: [
        "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>りそうです。",
        "<ruby>来年<rt>らいねん</rt></ruby>、<ruby>会社<rt>かいしゃ</rt></ruby>が<ruby>移動<rt>いどう</rt></ruby>するそうです。",
        "<ruby>彼女<rt>かのじょ</rt></ruby>は<ruby>来週<rt>らいしゅう</rt></ruby><ruby>結婚<rt>けっこん</rt></ruby>するらしいです。",
        "<ruby>携帯<rt>けいたい</rt></ruby>に<ruby>連絡<rt>れんらく</rt></ruby>したんですが、つながらなくて、<ruby>風邪<rt>かぜ</rt></ruby>をひいたみたいです。"
    ],
    10: [
        "<ruby>私<rt>わたし</rt></ruby>は<ruby>友達<rt>ともだち</rt></ruby>にケーキを<ruby>食<rt>た</rt></ruby>べられました。",
        "もう<ruby>少<rt>すこ</rt></ruby>し<ruby>考<rt>かんが</rt></ruby>えさせてください。",
        "<ruby>子<rt>こ</rt></ruby>どものころ、<ruby>毎日<rt>まいにち</rt></ruby>ピアノを<ruby>練習<rt>れんしゅう</rt></ruby>させられました。",
        "<ruby>実<rt>じつ</rt></ruby>は、<ruby>上司<rt>じょうし</rt></ruby>にひどいことを<ruby>言<rt>い</rt></ruby>われてしまいました。"
    ],
    11: [
        "<ruby>私<rt>わたし</rt></ruby>がおもちいたします。",
        "お<ruby>名前<rt>なまえ</rt></ruby>をおうかがいしてもよろしいでしょうか？",
        "いつもお<ruby>世話<rt>せわ</rt></ruby>になっております。",
        "レポートを<ruby>来週<rt>らいしゅう</rt></ruby>までに<ruby>提出<rt>ていしゅつ</rt></ruby>していただけますか？"
    ],
    12: [
        "<ruby>機械<rt>きかい</rt></ruby>が<ruby>壊<rt>こわ</rt></ruby>れてしまいまして･･･",
        "<ruby>上司<rt>じょうし</rt></ruby>に<ruby>残業<rt>ざんぎょう</rt></ruby>させられたため、<ruby>連絡<rt>れんらく</rt></ruby>が<ruby>遅<rt>おく</rt></ruby>れてしまいました。",
        "<ruby>予約<rt>よやく</rt></ruby>はしてあります。",
        "バックアップはとっておきました。"
    ],
    13: [
        "テクノロジーが<ruby>発達<rt>はったつ</rt></ruby>すればするほど、<ruby>人間<rt>にんげん</rt></ruby>の<ruby>仕事<rt>しごと</rt></ruby>が<ruby>減<rt>へ</rt></ruby>っていくと<ruby>考<rt>かんが</rt></ruby>えます。",
        "もし<ruby>世界中<rt>せかいじゅう</rt></ruby>が<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>話<rt>はな</rt></ruby>せるならば、<ruby>文化交流<rt>ぶんかこうりゅう</rt></ruby>がより<ruby>盛<rt>さか</rt></ruby>んになるでしょう。",
        "<ruby>私<rt>わたし</rt></ruby>はSNSは<ruby>若者<rt>わかもの</rt></ruby>に<ruby>悪<rt>わる</rt></ruby>い<ruby>影響<rt>えいきょう</rt></ruby>を<ruby>与<rt>あた</rt></ruby>えると<ruby>考<rt>かんが</rt></ruby>えます。",
        "<ruby>私<rt>わたし</rt></ruby>の<ruby>国<rt>くに</rt></ruby>と<ruby>比<rt>くら</rt></ruby>べると、<ruby>日本<rt>にほん</rt></ruby>のほうが <ruby>公共交通<rt>こうきょうこうつう</rt></ruby>が<ruby>発達<rt>はったつ</rt></ruby>していると<ruby>思<rt>おも</rt></ruby>います。"
    ]
}

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

for step_num, sentences in new_examples.items():
    step_key = f"pracStep{step_num:02d}"
    
    pattern = r"(" + step_key + r"\s*:\s*\{.*?\"examples\"\s*:\s*)(\[.*?\])(\s*,\s*\"quizzes\")"
    
    def repl(match):
        prefix = match.group(1)
        suffix = match.group(3)
        existing_json = match.group(2)
        try:
            ex_list = json.loads(existing_json)
        except Exception as e:
            print(f"Failed to parse json for {step_key}: {e}")
            return match.group(0)
            
        new_list = []
        for i, sent in enumerate(sentences):
            if i < len(ex_list):
                new_list.append({"jp": sent, "romaji": ex_list[i].get("romaji", ""), "en": ex_list[i].get("en", "")})
            else:
                new_list.append({"jp": sent, "romaji": "", "en": ""})
                
        return prefix + json.dumps(new_list, ensure_ascii=False) + suffix

    new_content, count = re.subn(pattern, repl, content, flags=re.DOTALL)
    if count == 0:
        print(f"Warning: Could not find/replace {step_key}")
    else:
        content = new_content

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done updating index.html with furigana")
