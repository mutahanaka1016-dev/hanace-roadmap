import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

updates = {
    "pracStep01": [
        "この<ruby>映画<rt>えいが</rt></ruby>はわたしが<ruby>選びました<rt>えらびました</rt></ruby>。",
        "<ruby>刺身<rt>さしみ</rt></ruby>は<ruby>食べます<rt>たべます</rt></ruby>。<ruby>肉<rt>にく</rt></ruby>は<ruby>食べません<rt>たべません</rt></ruby>。",
        "わたしは<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>難しい<rt>むずかしい</rt></ruby>と<ruby>思います<rt>おもいます</rt></ruby>。",
        "<ruby>実<rt>じつ</rt></ruby>は、<ruby>財布<rt>さいふ</rt></ruby>がみつかりました！<ruby>財布<rt>さいふ</rt></ruby>は<ruby>駅<rt>えき</rt></ruby>の<ruby>交番<rt>こうばん</rt></ruby>にありました。"
    ],
    "pracStep02": [
        "<ruby>東京<rt>とうきょう</rt></ruby>は<ruby>大阪<rt>おおさか</rt></ruby>ほど<ruby>食べ物<rt>たべもの</rt></ruby>がおいしくない。",
        "このクラスのなかで、<ruby>田中<rt>たなか</rt></ruby>さんがいちばん<ruby>頭<rt>あたま</rt></ruby>がいいです。",
        "<ruby>勉強<rt>べんきょう</rt></ruby>すればするほど、<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>上手<rt>じょうず</rt></ruby>になります。",
        "<ruby>便利<rt>べんり</rt></ruby>になればなるほど、<ruby>人間<rt>にんげん</rt></ruby>は<ruby>怠ける<rt>なまける</rt></ruby>ようになります。"
    ],
    "pracStep03": [
        "<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>話す<rt>はなす</rt></ruby>ことができます。",
        "ピアノを<ruby>弾く<rt>ひく</rt></ruby> ➡ ピアノが<ruby>弾けます<rt>ひけます</rt></ruby>",
        "<ruby>日本<rt>にほん</rt></ruby>に<ruby>行く<rt>いく</rt></ruby><ruby>前<rt>まえ</rt></ruby>は、<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>話せませんでした<rt>はなせませんでした</rt></ruby>。",
        "なっとうが<ruby>食べられます<rt>たべられます</rt></ruby>か？ ➡ はじめは<ruby>食べられません<rt>たべられません</rt></ruby>でしたが、いまは<ruby>食べられます<rt>たべられます</rt></ruby>！"
    ],
    "pracStep04": [
        "みぎにまわると、<ruby>郵便局<rt>ゆうびんきょく</rt></ruby>があります。",
        "お<ruby>金<rt>かね</rt></ruby>があれば、<ruby>旅行<rt>りょこう</rt></ruby>したいです。",
        "<ruby>日本<rt>にほん</rt></ruby>に<ruby>行く<rt>いく</rt></ruby>なら、<ruby>京都<rt>きょうと</rt></ruby>は<ruby>絶対<rt>ぜったい</rt></ruby>にいったほうがいいですよ。",
        "まいにち<ruby>日本語<rt>にほんご</rt></ruby>で<ruby>日記<rt>にっき</rt></ruby>を<ruby>書けば<rt>かけば</rt></ruby>、<ruby>絶対<rt>ぜったい</rt></ruby>にうまくなりますよ！"
    ],
    "pracStep05": [
        "<ruby>電車<rt>でんしゃ</rt></ruby>が<ruby>遅れました<rt>おくれました</rt></ruby>。それで、<ruby>会議<rt>かいぎ</rt></ruby>に<ruby>遅刻<rt>ちこく</rt></ruby>しました。",
        "この<ruby>計画<rt>けいかく</rt></ruby>はいいと<ruby>思います<rt>おもいます</rt></ruby>。けれど、<ruby>予算<rt>よさん</rt></ruby>が<ruby>足りません<rt>たりません</rt></ruby>。",
        "このアパートは<ruby>駅<rt>えき</rt></ruby>に<ruby>近い<rt>ちかい</rt></ruby>です。しかも、<ruby>安い<rt>やすい</rt></ruby>割です！",
        "<ruby>日本語<rt>にほんご</rt></ruby>は<ruby>難しい<rt>むずかしい</rt></ruby>です。けれど、とても<ruby>楽しい<rt>たのしい</rt></ruby>です。さらに、<ruby>勉強<rt>べんきょう</rt></ruby>すればするほど、<ruby>上手<rt>じょうず</rt></ruby>になります。だから、<ruby>毎日<rt>まいにち</rt></ruby><ruby>練習<rt>れんしゅう</rt></ruby>を<ruby>欠かしません<rt>かかしません</rt></ruby>。"
    ],
    "pracStep06": [
        "わざわざきてくださってありがとうございます。",
        "まどがあけてある。 （※<ruby>人間<rt>にんげん</rt></ruby>の<ruby>意図<rt>いと</rt></ruby>がある<ruby>準備状態<rt>じゅんびじょうたい</rt></ruby>）",
        "<ruby>旅行<rt>りょこう</rt></ruby>の<ruby>前<rt>まえ</rt></ruby>に、ホテルを<ruby>予約<rt>よやく</rt></ruby>しておきました。",
        "ケーキを<ruby>全部<rt>ぜんぶ</rt></ruby><ruby>食べてしまいました<rt>たべてしまいました</rt></ruby>。"
    ],
    "pracStep07": [
        "<ruby>先生<rt>せんせい</rt></ruby>はわたしにアドバイスをくれました。",
        "わたしは<ruby>先生<rt>せんせい</rt></ruby>にアドバイスをもらいました。",
        "<ruby>先生<rt>せんせい</rt></ruby>にアドバイスをいただきました。",
        "こんど<ruby>引っ越す<rt>ひっこす</rt></ruby>んですが、手伝ってもらえますか？ ➡ もちろん！よかったら、<ruby>荷物<rt>にもつ</rt></ruby>も<ruby>運んで<rt>はこんで</rt></ruby>あげますよ。"
    ],
    "pracStep08": [
        "おもちゃがこわれました。 （※<ruby>誰<rt>だれ</rt></ruby>のせいにもしない<ruby>表現<rt>ひょうげん</rt></ruby>）",
        "まどが<ruby>開けて<rt>あけて</rt></ruby>あります。 （※<ruby>他動詞<rt>たどうし</rt></ruby>＋てある：<ruby>誰<rt>だれ</rt></ruby>かが<ruby>意図的<rt>いとてき</rt></ruby>にやった<ruby>結果<rt>けっか</rt></ruby>）",
        "まどが<ruby>開いて<rt>あいて</rt></ruby>います。 （※<ruby>自動詞<rt>じどうし</rt></ruby>＋ている：ただの<ruby>現在<rt>げんざい</rt></ruby>の<ruby>状態<rt>じょうたい</rt></ruby>）",
        "このコップ、どうしたんですか？ ➡ あの…おちてしまって、われてしまいました。"
    ],
    "pracStep09": [
        "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降りそうです<rt>ふりそうです</rt></ruby>。 （※見た目の<ruby>印象<rt>いんしょう</rt></ruby>：STEM ＋ そうだ）",
        "<ruby>来年<rt>らいねん</rt></ruby>、<ruby>会社<rt>かいしゃ</rt></ruby>が<ruby>移動<rt>いどう</rt></ruby>になるそうです。 （※人から聞いた話：<ruby>普通形<rt>ふつうけい</rt></ruby> ＋ そうだ）",
        "<ruby>彼女<rt>かのじょ</rt></ruby>は<ruby>来週<rt>らいしゅう</rt></ruby><ruby>結婚する<rt>けっこんする</rt></ruby>らしいです。 （※外からの<ruby>噂<rt>うわさ</rt></ruby>や<ruby>情報<rt>じょうほう</rt></ruby>：<ruby>普通形<rt>ふつうけい</rt></ruby> ＋ らしい）",
        "<ruby>携帯<rt>けいたい</rt></ruby>に<ruby>連絡<rt>れんらく</rt></ruby>したんですが、つながらなくて、<ruby>風邪<rt>かぜ</rt></ruby>をひいたみたいです。 （※<ruby>状況<rt>じょうきょう</rt></ruby>からの<ruby>推論<rt>すいろん</rt></ruby>）"
    ],
    "pracStep10": [
        "わたしは<ruby>友達<rt>ともだち</rt></ruby>にケーキをたべられました。 （※<ruby>間接受身<rt>かんせつうけみ</rt></ruby>：迷惑のニュアンス）",
        "もうすこし考えさせてください。 （※<ruby>使役形<rt>しえきけい</rt></ruby>を使った定番の<ruby>許可<rt>きょか</rt></ruby>申請）",
        "子どものころ、まいにちピアノをれんしゅうさせられました。 （※<ruby>使役受身<rt>しえきうけみけい</rt></ruby>：嫌々やった）",
        "実は、じょうしにひどいことをいわれてしまいました。それに、しごとをやめさせられそうになりました。"
    ],
    "pracStep11": [
        "わたしがおもちいたします。",
        "お名前をおうかがいしてもよろしいでしょうか？",
        "いつもおせわになっております。",
        "レポートをらいしゅうまでに<ruby>提出して<rt>ていしゅつして</rt></ruby>いただけますか？ ➡ かしこまりました。らいしゅうの金曜日までに<ruby>提出いたします<rt>ていしゅついたします</rt></ruby>。"
    ],
    "pracStep12": [
        "<ruby>機械<rt>きかい</rt></ruby>がこわれてしまいまして･･･ （※お詫びの前のクッション言葉）",
        "じょうしに<ruby>残業<rt>ざんぎょう</rt></ruby>させられたため、れんらくがおくれてしまいました。",
        "よやくを<ruby>承って<rt>うけたまわって</rt></ruby>おりましたが、システムのえらーにより、よやくじょうほうがきえてしまいまして、おへやの<ruby>ご用意<rt>ごようい</rt></ruby>ができておりませんでした。",
        "<ruby>報告書<rt>ほうこくしょ</rt></ruby>はせんしゅうまでに完成させておく予定でおりましたが、<ruby>急遽<rt>きゅうきょ</rt></ruby>たのまれた別の仕事に<ruby>取りかからせられて<rt>とりかからせられて</rt></ruby>しまいまして、提出がおくれてしまいました。"
    ],
    "pracStep13": [
        "テクノロジーが発達すればするほど、にんげんの仕事がへっていくと<ruby>考えます<rt>かんがえます</rt></ruby>。",
        "もしせかいじゅうが<ruby>日本語<rt>にほんご</rt></ruby>を話せるならば、ぶんかこうりゅうがより盛んになるでしょう。",
        "私はSNSはわかものに悪い影響を与えると<ruby>考えます<rt>かんがえます</rt></ruby>。なぜなら、SNSは<ruby>自己評価<rt>じこひょうか</rt></ruby>を低くさせるからです。たしかに便利ですが…したがって、<ruby>規制<rt>きせい</rt></ruby>が必要ではないでしょうか。",
        "あたらしいテクノロジーはあたらしい仕事も生み出すという研究もあります。したがって、仕事が「うばう」のではなく、にんげんの役割が「かわっていく」というほうが正確ではないでしょうか。"
    ]
}

def replace_examples(m):
    step_id = m.group(1)
    if step_id in updates:
        exs = [{"jp": new_jp, "romaji": "", "en": ""} for new_jp in updates[step_id]]
        exs_str = json.dumps(exs, ensure_ascii=False)
        return f'{step_id}: {m.group(2)}"examples": {exs_str}'
    return m.group(0)

new_text, count = re.subn(r'(pracStep\d{2}):\s*(\{.*?)"examples":\s*\[.*?\]', replace_examples, text, flags=re.DOTALL)
print(f"Replaced {count} instances.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

