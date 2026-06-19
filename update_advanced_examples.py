import re
import json

new_examples = {
    1: [
        "この映画は私が選びました。",
        "刺身は食べます。肉は食べません。",
        "私は日本語が難しいと思います。",
        "実は、財布がみつかりました！財布は駅の交番にありました。"
    ],
    2: [
        "東京は大阪ほど食べ物がおいしくない。",
        "このクラスのなかで、田中さんがいちばん頭がいいです。",
        "勉強すればするほど、日本語が上手になります。",
        "便利になればなるほど、人間は怠けるようになります。"
    ],
    3: [
        "日本語を話すことができます。",
        "ピアノが弾けます",
        "日本に行く前は、日本語が話せませんでした。",
        "なっとうが食べられますか？"
    ],
    4: [
        "右に回ると、郵便局があります。",
        "お金があれば、旅行したいです。",
        "日本に行くなら、京都は絶対に行ったほうがいいですよ。",
        "毎日日本語で日記を書けば、絶対にうまくなりますよ！"
    ],
    5: [
        "電車が遅れました。それで、会議に遅刻しました。",
        "この計画はいいと思います。けれど、予算が足りません。",
        "このアパートは駅に近いです。しかも、安いです！",
        "日本語は難しいです。けれど、とても楽しいです。さらに、勉強すればするほど、上手になります。だから、毎日練習を欠かしません。"
    ],
    6: [
        "わざわざ来てくださってありがとうございます。",
        "窓があけてある。",
        "旅行の前に、ホテルを予約しておきました。",
        "ケーキを全部食べてしまいました。"
    ],
    7: [
        "先生は私にアドバイスをくれました。",
        "私は先生にアドバイスをもらいました。",
        "先生にアドバイスをいただきました。",
        "今度、引っ越すんですが、手伝ってもらえますか？"
    ],
    8: [
        "おもちゃが壊れました。",
        "おもちゃを壊しました。",
        "窓が開けてあります。",
        "窓が開いています。"
    ],
    9: [
        "雨が降りそうです。",
        "来年、会社が移動するそうです。",
        "彼女は来週結婚するらしいです。",
        "携帯に連絡したんですが、つながらなくて、風邪をひいたみたいです。"
    ],
    10: [
        "私は友達にケーキを食べられました。",
        "もう少し考えさせてください。",
        "子どものころ、毎日ピアノを練習させられました。",
        "実は、上司にひどいことを言われてしまいました。"
    ],
    11: [
        "私がおもちいたします。",
        "お名前をおうかがいしてもよろしいでしょうか？",
        "いつもお世話になっております。",
        "レポートを来週までに提出していただけますか？"
    ],
    12: [
        "機械が壊れてしまいまして･･･",
        "上司に残業させられたため、連絡が遅れてしまいました。",
        "予約はしてあります。",
        "バックアップはとっておきました。"
    ],
    13: [
        "テクノロジーが発達すればするほど、人間の仕事が減っていくと考えます。",
        "もし世界中が日本語を話せるならば、文化交流がより盛んになるでしょう。",
        "私はSNSは若者に悪い影響を与えると考えます。",
        "私の国と比べると、日本のほうが 公共交通が発達していると思います。"
    ]
}

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

for step_num, sentences in new_examples.items():
    step_key = f"pracStep{step_num:02d}"
    
    # We look for pracStepXX: { ... "examples": [...], "quizzes"
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

print("Done updating index.html")
