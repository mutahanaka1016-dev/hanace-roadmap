import json
import random

def generate_questions(level, vocab_items, grammar_items):
    questions = []
    
    # 20 Vocab/Language questions
    for i in range(20):
        item = vocab_items[i % len(vocab_items)]
        # Generate some dummy incorrect options by shuffling other vocab meanings
        other_meanings = [v['meaning'] for v in vocab_items if v != item]
        random.shuffle(other_meanings)
        options = [item['meaning']] + other_meanings[:3]
        random.shuffle(options)
        answer_index = options.index(item['meaning'])
        
        q = {
            "id": f"{level}_v_{i+1}",
            "category": "vocab",
            "question": f"What is the meaning of '{item['word']}'?",
            "options": options,
            "answer": answer_index,
            "explanation": f"'{item['word']}' means '{item['meaning']}'."
        }
        questions.append(q)
        
    # 20 Grammar/Reading questions
    for i in range(20):
        item = grammar_items[i % len(grammar_items)]
        other_options = [g['incorrect'] for g in grammar_items if g != item]
        # flatten and sample
        flat_others = [opt for sublist in other_options for opt in sublist]
        random.shuffle(flat_others)
        
        options = [item['correct']] + item['incorrect'][:3]
        if len(options) < 4:
            options += flat_others[:4-len(options)]
            
        random.shuffle(options)
        answer_index = options.index(item['correct'])
        
        q = {
            "id": f"{level}_g_{i+1}",
            "category": "grammar",
            "question": item['question'],
            "options": options,
            "answer": answer_index,
            "explanation": item['explanation']
        }
        questions.append(q)
        
    return questions

# Beginner Data
beg_vocab = [
    {"word": "<ruby>犬<rt>いぬ</rt></ruby>", "meaning": "Dog"},
    {"word": "<ruby>猫<rt>ねこ</rt></ruby>", "meaning": "Cat"},
    {"word": "<ruby>食<rt>た</rt></ruby>べる", "meaning": "To eat"},
    {"word": "<ruby>飲<rt>の</rt></ruby>む", "meaning": "To drink"},
    {"word": "<ruby>行<rt>い</rt></ruby>く", "meaning": "To go"},
    {"word": "<ruby>本<rt>ほん</rt></ruby>", "meaning": "Book"},
    {"word": "<ruby>車<rt>くるま</rt></ruby>", "meaning": "Car"},
    {"word": "<ruby>水<rt>みず</rt></ruby>", "meaning": "Water"},
    {"word": "<ruby>先生<rt>せんせい</rt></ruby>", "meaning": "Teacher"},
    {"word": "<ruby>学生<rt>がくせい</rt></ruby>", "meaning": "Student"},
    {"word": "<ruby>学校<rt>がっこう</rt></ruby>", "meaning": "School"},
    {"word": "<ruby>今日<rt>きょう</rt></ruby>", "meaning": "Today"},
    {"word": "<ruby>明日<rt>あした</rt></ruby>", "meaning": "Tomorrow"},
    {"word": "<ruby>昨日<rt>きのう</rt></ruby>", "meaning": "Yesterday"},
    {"word": "<ruby>大<rt>おお</rt></ruby>きい", "meaning": "Big"},
    {"word": "<ruby>小<rt>ちい</rt></ruby>さい", "meaning": "Small"},
    {"word": "<ruby>新<rt>あたら</rt></ruby>しい", "meaning": "New"},
    {"word": "<ruby>古<rt>ふる</rt></ruby>い", "meaning": "Old"},
    {"word": "<ruby>高<rt>たか</rt></ruby>い", "meaning": "High/Expensive"},
    {"word": "<ruby>安<rt>やす</rt></ruby>い", "meaning": "Cheap"}
]

beg_grammar = [
    {"question": "Choose the correct particle: わたし ___ <ruby>学生<rt>がくせい</rt></ruby>です。", "correct": "は", "incorrect": ["が", "を", "に"], "explanation": "The particle 'は' (wa) marks the topic of the sentence."},
    {"question": "How do you say 'It is not a dog'?", "correct": "<ruby>犬<rt>いぬ</rt></ruby>ではありません", "incorrect": ["<ruby>犬<rt>いぬ</rt></ruby>です", "<ruby>犬<rt>いぬ</rt></ruby>でした", "<ruby>犬<rt>いぬ</rt></ruby>ではありませんでした"], "explanation": "'ではありません' is the present negative form for nouns."},
    {"question": "What is the past tense of '<ruby>食<rt>た</rt></ruby>べる' (to eat) in polite form?", "correct": "<ruby>食<rt>た</rt></ruby>べました", "incorrect": ["<ruby>食<rt>た</rt></ruby>べます", "<ruby>食<rt>た</rt></ruby>べません", "<ruby>食<rt>た</rt></ruby>べませんでした"], "explanation": "'ました' is the polite past tense suffix."},
    {"question": "Choose the correct particle: りんご ___ <ruby>食<rt>た</rt></ruby>べます。", "correct": "を", "incorrect": ["は", "が", "に"], "explanation": "The particle 'を' (o) marks the direct object."},
    {"question": "What is the past negative of '<ruby>学生<rt>がくせい</rt></ruby>です'?", "correct": "<ruby>学生<rt>がくせい</rt></ruby>ではありませんでした", "incorrect": ["<ruby>学生<rt>がくせい</rt></ruby>でした", "<ruby>学生<rt>がくせい</rt></ruby>ではありません", "<ruby>学生<rt>がくせい</rt></ruby>です"], "explanation": "'ではありませんでした' is the past negative form for nouns."},
    {"question": "Translate: 'I went to the school.'", "correct": "<ruby>学校<rt>がっこう</rt></ruby>に<ruby>行<rt>い</rt></ruby>きました。", "incorrect": ["<ruby>学校<rt>がっこう</rt></ruby>に<ruby>行<rt>い</rt></ruby>きます。", "<ruby>学校<rt>がっこう</rt></ruby>に<ruby>来<rt>き</rt></ruby>ました。", "<ruby>学校<rt>がっこう</rt></ruby>に<ruby>行<rt>い</rt></ruby>きません。"], "explanation": "<ruby>行<rt>い</rt></ruby>きました is the past tense of 'to go'."},
    {"question": "Which particle indicates destination?", "correct": "に", "incorrect": ["を", "が", "の"], "explanation": "'に' or 'へ' marks the destination of movement."},
    {"question": "How do you say 'Let's eat!'?", "correct": "<ruby>食<rt>た</rt></ruby>べましょう", "incorrect": ["<ruby>食<rt>た</rt></ruby>べます", "<ruby>食<rt>た</rt></ruby>べて", "<ruby>食<rt>た</rt></ruby>べたい"], "explanation": "'〜ましょう' means 'Let's ~'."},
    {"question": "Translate: 'This is my book.'", "correct": "これはわたしの<ruby>本<rt>ほん</rt></ruby>です。", "incorrect": ["これはわたし<ruby>本<rt>ほん</rt></ruby>です。", "わたしはこれの<ruby>本<rt>ほん</rt></ruby>です。", "これは<ruby>本<rt>ほん</rt></ruby>わたしです。"], "explanation": "'の' connects nouns to show possession."},
    {"question": "Which adjective means 'delicious'?", "correct": "おいしい", "incorrect": ["<ruby>大<rt>おお</rt></ruby>きい", "たのしい", "むずかしい"], "explanation": "'おいしい' means delicious."},
    {"question": "What is the Te-form of '<ruby>食<rt>た</rt></ruby>べる'?", "correct": "<ruby>食<rt>た</rt></ruby>べて", "incorrect": ["<ruby>食<rt>た</rt></ruby>べって", "<ruby>食<rt>た</rt></ruby>べんで", "<ruby>食<rt>た</rt></ruby>べいて"], "explanation": "Ru-verbs like '<ruby>食<rt>た</rt></ruby>べる' simply replace 'る' with 'て'."},
    {"question": "What is the Te-form of '<ruby>飲<rt>の</rt></ruby>む'?", "correct": "<ruby>飲<rt>の</rt></ruby>んで", "incorrect": ["<ruby>飲<rt>の</rt></ruby>みて", "<ruby>飲<rt>の</rt></ruby>って", "<ruby>飲<rt>の</rt></ruby>いて"], "explanation": "Verbs ending in 'む' become 'んで' in Te-form."},
    {"question": "Choose the correct particle: <ruby>東京<rt>とうきょう</rt></ruby> ___ <ruby>行<rt>い</rt></ruby>きます。", "correct": "に", "incorrect": ["を", "が", "で"], "explanation": "Particle 'に' indicates destination."},
    {"question": "Translate: 'Please eat.'", "correct": "<ruby>食<rt>た</rt></ruby>べてください", "incorrect": ["<ruby>食<rt>た</rt></ruby>べます", "<ruby>食<rt>た</rt></ruby>べましょう", "<ruby>食<rt>た</rt></ruby>べたい"], "explanation": "Te-form + ください means 'Please do ~'."},
    {"question": "How do you say 'want to eat'?", "correct": "<ruby>食<rt>た</rt></ruby>べたい", "incorrect": ["<ruby>食<rt>た</rt></ruby>べます", "<ruby>食<rt>た</rt></ruby>べて", "<ruby>食<rt>た</rt></ruby>べましょう"], "explanation": "Stem + 'たい' expresses desire."},
    {"question": "Choose the correct counter for small objects (like an apple): りんごを２___ください。", "correct": "つ", "incorrect": ["<ruby>本<rt>ほん</rt></ruby>", "<ruby>枚<rt>まい</rt></ruby>", "<ruby>人<rt>にん</rt></ruby>"], "explanation": "'つ' is the general counter for small or abstract objects."},
    {"question": "How do you say 'I am currently eating'?", "correct": "<ruby>食<rt>た</rt></ruby>べています", "incorrect": ["<ruby>食<rt>た</rt></ruby>べます", "<ruby>食<rt>た</rt></ruby>べました", "<ruby>食<rt>た</rt></ruby>べたいです"], "explanation": "Te-form + 'います' expresses ongoing action."},
    {"question": "What is the negative form of 'おいしい' (delicious)?", "correct": "おいしくない", "incorrect": ["おいしいじゃない", "おいしくありませんでした", "おいしいくない"], "explanation": "For i-adjectives, drop 'い' and add 'くない'."},
    {"question": "Translate: 'It was fun.' (たのしい)", "correct": "たのしかったです", "incorrect": ["たのしいでした", "たのしくないです", "たのしかった"], "explanation": "For i-adjectives, past tense is formed by dropping 'い' and adding 'かった'."},
    {"question": "Choose the correct particle: ペン ___ <ruby>書<rt>か</rt></ruby>きます。", "correct": "で", "incorrect": ["に", "を", "が"], "explanation": "Particle 'で' indicates the tool or means used."}
]

int_vocab = [
    {"word": "<ruby>経済<rt>けいざい</rt></ruby>", "meaning": "Economy"},
    {"word": "<ruby>政治<rt>せいじ</rt></ruby>", "meaning": "Politics"},
    {"word": "<ruby>経験<rt>けいけん</rt></ruby>", "meaning": "Experience"},
    {"word": "<ruby>理由<rt>りゆう</rt></ruby>", "meaning": "Reason"},
    {"word": "<ruby>意見<rt>いけん</rt></ruby>", "meaning": "Opinion"},
    {"word": "<ruby>結果<rt>けっか</rt></ruby>", "meaning": "Result"},
    {"word": "<ruby>計画<rt>けいかく</rt></ruby>", "meaning": "Plan"},
    {"word": "<ruby>問題<rt>もんだい</rt></ruby>", "meaning": "Problem"},
    {"word": "<ruby>質問<rt>しつもん</rt></ruby>", "meaning": "Question"},
    {"word": "<ruby>答<rt>こた</rt></ruby>え", "meaning": "Answer"},
    {"word": "<ruby>旅行<rt>りょこう</rt></ruby>", "meaning": "Travel"},
    {"word": "<ruby>準備<rt>じゅんび</rt></ruby>", "meaning": "Preparation"},
    {"word": "<ruby>約束<rt>やくそく</rt></ruby>", "meaning": "Promise / Appointment"},
    {"word": "<ruby>趣味<rt>しゅみ</rt></ruby>", "meaning": "Hobby"},
    {"word": "<ruby>目的<rt>もくてき</rt></ruby>", "meaning": "Purpose"},
    {"word": "<ruby>文化<rt>ぶんか</rt></ruby>", "meaning": "Culture"},
    {"word": "<ruby>社会<rt>しゃかい</rt></ruby>", "meaning": "Society"},
    {"word": "<ruby>自然<rt>しぜん</rt></ruby>", "meaning": "Nature"},
    {"word": "<ruby>環境<rt>かんきょう</rt></ruby>", "meaning": "Environment"},
    {"word": "<ruby>生活<rt>せいかつ</rt></ruby>", "meaning": "Lifestyle / Daily life"}
]

int_grammar = [
    {"question": "Which conjunction means 'However'?", "correct": "しかし", "incorrect": ["だから", "そして", "すると"], "explanation": "'しかし' translates to 'however'."},
    {"question": "How do you say 'I can speak Japanese'?", "correct": "<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>話<rt>はな</rt></ruby>せます", "incorrect": ["<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>話<rt>はな</rt></ruby>します", "<ruby>日本語<rt>にほんご</rt></ruby>が<ruby>話<rt>はな</rt></ruby>します", "<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>話<rt>はな</rt></ruby>せます"], "explanation": "The potential form '<ruby>話<rt>はな</rt></ruby>せる' takes the particle 'が'."},
    {"question": "Translate: 'If it rains, I won't go.'", "correct": "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>ったら、<ruby>行<rt>い</rt></ruby>きません", "incorrect": ["<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>っても、<ruby>行<rt>い</rt></ruby>きません", "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るので、<ruby>行<rt>い</rt></ruby>きません", "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るのに、<ruby>行<rt>い</rt></ruby>きません"], "explanation": "'〜たら' is the conditional 'if'."},
    {"question": "What does '〜ても' mean?", "correct": "Even if", "incorrect": ["Because", "If", "When"], "explanation": "'〜ても' expresses 'even if / even though'."},
    {"question": "How do you say 'I must study'?", "correct": "<ruby>勉強<rt>べんきょう</rt></ruby>しなければなりません", "incorrect": ["<ruby>勉強<rt>べんきょう</rt></ruby>してはいけません", "<ruby>勉強<rt>べんきょう</rt></ruby>してもいいです", "<ruby>勉強<rt>べんきょう</rt></ruby>するつもりです"], "explanation": "'〜なければなりません' means 'must do'."},
    {"question": "Which verb is intransitive?", "correct": "<ruby>開<rt>あ</rt></ruby>く", "incorrect": ["<ruby>開<rt>あ</rt></ruby>ける", "<ruby>閉<rt>し</rt></ruby>める", "<ruby>壊<rt>こわ</rt></ruby>す"], "explanation": "'<ruby>開<rt>あ</rt></ruby>く' (to open by itself) is intransitive."},
    {"question": "Translate: 'The window is left open (intentionally).'", "correct": "<ruby>窓<rt>まど</rt></ruby>が<ruby>開<rt>あ</rt></ruby>けてあります", "incorrect": ["<ruby>窓<rt>まど</rt></ruby>が<ruby>開<rt>あ</rt></ruby>いています", "<ruby>窓<rt>まど</rt></ruby>が<ruby>開<rt>あ</rt></ruby>きます", "<ruby>窓<rt>まど</rt></ruby>が<ruby>開<rt>あ</rt></ruby>けます"], "explanation": "Transitive Te-form + 'ある' indicates a state resulting from an intentional action."},
    {"question": "Translate: 'I received a book from the teacher.' (Humble)", "correct": "<ruby>先生<rt>せんせい</rt></ruby>に<ruby>本<rt>ほん</rt></ruby>をいただきました", "incorrect": ["<ruby>先生<rt>せんせい</rt></ruby>に<ruby>本<rt>ほん</rt></ruby>をもらいました", "<ruby>先生<rt>せんせい</rt></ruby>に<ruby>本<rt>ほん</rt></ruby>をくれました", "<ruby>先生<rt>せんせい</rt></ruby>に<ruby>本<rt>ほん</rt></ruby>をあげました"], "explanation": "'いただく' is the humble form of 'もらう' (to receive)."},
    {"question": "Translate: 'The teacher gave me a book.' (Honorific)", "correct": "<ruby>先生<rt>せんせい</rt></ruby>が<ruby>本<rt>ほん</rt></ruby>をくださいました", "incorrect": ["<ruby>先生<rt>せんせい</rt></ruby>が<ruby>本<rt>ほん</rt></ruby>をくれました", "<ruby>先生<rt>せんせい</rt></ruby>が<ruby>本<rt>ほん</rt></ruby>をあげました", "<ruby>先生<rt>せんせい</rt></ruby>が<ruby>本<rt>ほん</rt></ruby>をいただきました"], "explanation": "'くださる' is the honorific form of 'くれる' (to give to me)."},
    {"question": "How do you say 'It seems to be raining' (Conjecture based on evidence)?", "correct": "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>っているようです", "incorrect": ["<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るそうです", "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るはずです", "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るかもしれません"], "explanation": "'〜ようです' indicates a conjecture based on observation."},
    {"question": "Translate: 'I heard that it will rain tomorrow.' (Hearsay)", "correct": "<ruby>明日<rt>あした</rt></ruby>は<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るそうです", "incorrect": ["<ruby>明日<rt>あした</rt></ruby>は<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るようです", "<ruby>明日<rt>あした</rt></ruby>は<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るはずです", "<ruby>明日<rt>あした</rt></ruby>は<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るかもしれません"], "explanation": "'〜そうです' attached to plain form expresses hearsay ('I heard that...')."},
    {"question": "Which expresses 'Which is larger, A or B?'", "correct": "AとBとどちらが<ruby>大<rt>おお</rt></ruby>きいですか", "incorrect": ["AはBより<ruby>大<rt>おお</rt></ruby>きいです", "AはBほど<ruby>大<rt>おお</rt></ruby>きくないです", "Aの<ruby>中<rt>なか</rt></ruby>でBが<ruby>一番大<rt>いちばんおお</rt></ruby>きいです"], "explanation": "To compare two items, use 'AとBとどちらが〜'"},
    {"question": "Translate: 'A is larger than B.'", "correct": "AはBより<ruby>大<rt>おお</rt></ruby>きいです", "incorrect": ["AとBとどちらが<ruby>大<rt>おお</rt></ruby>きいです", "BはAより<ruby>大<rt>おお</rt></ruby>きいです", "AはBほど<ruby>大<rt>おお</rt></ruby>きくないです"], "explanation": "'AはBより〜' means 'A is more ~ than B'."},
    {"question": "Translate: 'I am planning to go to Japan.'", "correct": "<ruby>日本<rt>にほん</rt></ruby>へ<ruby>行<rt>い</rt></ruby>くつもりです", "incorrect": ["<ruby>日本<rt>にほん</rt></ruby>へ<ruby>行<rt>い</rt></ruby>くはずです", "<ruby>日本<rt>にほん</rt></ruby>へ<ruby>行<rt>い</rt></ruby>くかもしれません", "<ruby>日本<rt>にほん</rt></ruby>へ<ruby>行<rt>い</rt></ruby>くそうです"], "explanation": "'〜つもりです' expresses an intention or plan."},
    {"question": "Translate: 'You had better go to the hospital.'", "correct": "<ruby>病院<rt>びょういん</rt></ruby>に<ruby>行<rt>い</rt></ruby>ったほうがいいですよ", "incorrect": ["<ruby>病院<rt>びょういん</rt></ruby>に<ruby>行<rt>い</rt></ruby>かないほうがいいですよ", "<ruby>病院<rt>びょういん</rt></ruby>に<ruby>行<rt>い</rt></ruby>くはずです", "<ruby>病院<rt>びょういん</rt></ruby>に<ruby>行<rt>い</rt></ruby>くかもしれません"], "explanation": "Past plain form + 'ほうがいい' means 'You had better...'."},
    {"question": "Translate: 'It might rain.'", "correct": "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るかもしれません", "incorrect": ["<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るはずです", "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るそうです", "<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>るようです"], "explanation": "'〜かもしれません' means 'might / maybe'."},
    {"question": "How do you say 'I accidentally broke the cup'?", "correct": "コップを<ruby>割<rt>わ</rt></ruby>ってしまいました", "incorrect": ["コップを<ruby>割<rt>わ</rt></ruby>っておきました", "コップを<ruby>割<rt>わ</rt></ruby>ってありました", "コップを<ruby>割<rt>わ</rt></ruby>っていました"], "explanation": "Te-form + 'しまう' expresses regret or accidental completion."},
    {"question": "How do you say 'I booked the hotel in advance'?", "correct": "ホテルを<ruby>予約<rt>よやく</rt></ruby>しておきました", "incorrect": ["ホテルを<ruby>予約<rt>よやく</rt></ruby>してしまいました", "ホテルを<ruby>予約<rt>よやく</rt></ruby>してありました", "ホテルを<ruby>予約<rt>よやく</rt></ruby>しています"], "explanation": "Te-form + 'おく' means doing something in advance for preparation."},
    {"question": "Translate: 'Because it was cold, I didn't go out.'", "correct": "<ruby>寒<rt>さむ</rt></ruby>かったので、<ruby>出<rt>で</rt></ruby>かけませんでした", "incorrect": ["<ruby>寒<rt>さむ</rt></ruby>いから、<ruby>出<rt>で</rt></ruby>かけます", "<ruby>寒<rt>さむ</rt></ruby>くても、<ruby>出<rt>で</rt></ruby>かけませんでした", "<ruby>寒<rt>さむ</rt></ruby>かったのに、<ruby>出<rt>で</rt></ruby>かけませんでした"], "explanation": "'〜ので' is a polite way to express a reason ('because')."},
    {"question": "Translate: 'Even though I studied, I failed the test.'", "correct": "<ruby>勉強<rt>べんきょう</rt></ruby>したのに、テストに<ruby>落<rt>お</rt></ruby>ちました", "incorrect": ["<ruby>勉強<rt>べんきょう</rt></ruby>したので、テストに<ruby>落<rt>お</rt></ruby>ちました", "<ruby>勉強<rt>べんきょう</rt></ruby>したら、テストに<ruby>落<rt>お</rt></ruby>ちました", "<ruby>勉強<rt>べんきょう</rt></ruby>すれば、テストに<ruby>落<rt>お</rt></ruby>ちました"], "explanation": "'〜のに' expresses 'even though / despite'."}
]

adv_vocab = [
    {"word": "<ruby>抽象的<rt>ちゅうしょうてき</rt></ruby>", "meaning": "Abstract"},
    {"word": "<ruby>具体的<rt>ぐたいてき</rt></ruby>", "meaning": "Concrete / Specific"},
    {"word": "<ruby>矛盾<rt>むじゅん</rt></ruby>", "meaning": "Contradiction"},
    {"word": "<ruby>妥協<rt>だきょう</rt></ruby>", "meaning": "Compromise"},
    {"word": "<ruby>貢献<rt>こうけん</rt></ruby>", "meaning": "Contribution"},
    {"word": "<ruby>影響<rt>えいきょう</rt></ruby>", "meaning": "Influence / Effect"},
    {"word": "<ruby>象徴<rt>しょうちょう</rt></ruby>", "meaning": "Symbol"},
    {"word": "<ruby>傾向<rt>けいこう</rt></ruby>", "meaning": "Tendency / Trend"},
    {"word": "<ruby>評価<rt>ひょうか</rt></ruby>", "meaning": "Evaluation"},
    {"word": "<ruby>責任<rt>せきにん</rt></ruby>", "meaning": "Responsibility"},
    {"word": "<ruby>権利<rt>けんり</rt></ruby>", "meaning": "Right / Privilege"},
    {"word": "<ruby>義務<rt>ぎむ</rt></ruby>", "meaning": "Duty / Obligation"},
    {"word": "<ruby>価値観<rt>かちかん</rt></ruby>", "meaning": "Values"},
    {"word": "<ruby>現象<rt>げんしょう</rt></ruby>", "meaning": "Phenomenon"},
    {"word": "<ruby>概念<rt>がいねん</rt></ruby>", "meaning": "Concept"},
    {"word": "<ruby>基準<rt>きじゅん</rt></ruby>", "meaning": "Standard / Criteria"},
    {"word": "<ruby>構造<rt>こうぞう</rt></ruby>", "meaning": "Structure"},
    {"word": "<ruby>制度<rt>せいど</rt></ruby>", "meaning": "System / Institution"},
    {"word": "<ruby>哲学<rt>てつがく</rt></ruby>", "meaning": "Philosophy"},
    {"word": "<ruby>倫理<rt>りんり</rt></ruby>", "meaning": "Ethics"}
]

adv_grammar = [
    {"question": "Choose the correct usage of '〜ざるを<ruby>得<rt>え</rt></ruby>ない'.", "correct": "<ruby>彼<rt>かれ</rt></ruby>が<ruby>来<rt>こ</rt></ruby>ないなら、<ruby>私<rt>わたし</rt></ruby>が<ruby>行<rt>い</rt></ruby>かざるを<ruby>得<rt>え</rt></ruby>ない。", "incorrect": ["<ruby>彼<rt>かれ</rt></ruby>が<ruby>来<rt>こ</rt></ruby>ないなら、<ruby>私<rt>わたし</rt></ruby>が<ruby>行<rt>い</rt></ruby>くざるを<ruby>得<rt>え</rt></ruby>ない。", "<ruby>彼<rt>かれ</rt></ruby>が<ruby>来<rt>こ</rt></ruby>ないなら、<ruby>私<rt>わたし</rt></ruby>が<ruby>行<rt>い</rt></ruby>こざるを<ruby>得<rt>え</rt></ruby>ない。", "<ruby>彼<rt>かれ</rt></ruby>が<ruby>来<rt>こ</rt></ruby>ないなら、<ruby>私<rt>わたし</rt></ruby>が<ruby>行<rt>い</rt></ruby>きざるを<ruby>得<rt>え</rt></ruby>ない。"], "explanation": "'〜ざるを<ruby>得<rt>え</rt></ruby>ない' means 'have no choice but to'. It attaches to the Nai-stem of verbs."},
    {"question": "What does '〜に<ruby>違<rt>ちが</rt></ruby>いない' mean?", "correct": "Must be / Without a doubt", "incorrect": ["Might be", "Should not be", "Used to be"], "explanation": "'〜に<ruby>違<rt>ちが</rt></ruby>いない' expresses strong conviction or certainty."},
    {"question": "Translate: 'Depending on the person, opinions differ.'", "correct": "<ruby>人<rt>ひと</rt></ruby>によって<ruby>意見<rt>いけん</rt></ruby>が<ruby>違<rt>ちが</rt></ruby>う。", "incorrect": ["<ruby>人<rt>ひと</rt></ruby>について<ruby>意見<rt>いけん</rt></ruby>が<ruby>違<rt>ちが</rt></ruby>う。", "<ruby>人<rt>ひと</rt></ruby>にとって<ruby>意見<rt>いけん</rt></ruby>が<ruby>違<rt>ちが</rt></ruby>う。", "<ruby>人<rt>ひと</rt></ruby>として<ruby>意見<rt>いけん</rt></ruby>が<ruby>違<rt>ちが</rt></ruby>う。"], "explanation": "'〜によって' means 'depending on' or 'due to'."},
    {"question": "Translate: 'For me, this book is difficult.'", "correct": "<ruby>私<rt>わたし</rt></ruby>にとって、この<ruby>本<rt>ほん</rt></ruby>は<ruby>難<rt>むずか</rt></ruby>しい。", "incorrect": ["<ruby>私<rt>わたし</rt></ruby>によって、この<ruby>本<rt>ほん</rt></ruby>は<ruby>難<rt>むずか</rt></ruby>しい。", "<ruby>私<rt>わたし</rt></ruby>について、この<ruby>本<rt>ほん</rt></ruby>は<ruby>難<rt>むずか</rt></ruby>しい。", "<ruby>私<rt>わたし</rt></ruby>として、この<ruby>本<rt>ほん</rt></ruby>は<ruby>難<rt>むずか</rt></ruby>しい。"], "explanation": "'〜にとって' means 'for / from the perspective of'."},
    {"question": "Choose the correct usage of '〜にかかわらず'.", "correct": "<ruby>天候<rt>てんこう</rt></ruby>にかかわらず、<ruby>試合<rt>しあい</rt></ruby>は<ruby>行<rt>おこな</rt></ruby>われます。", "incorrect": ["<ruby>天候<rt>てんこう</rt></ruby>にかかわって、<ruby>試合<rt>しあい</rt></ruby>は<ruby>行<rt>おこな</rt></ruby>われます。", "<ruby>天候<rt>てんこう</rt></ruby>にかかわりなくは、<ruby>試合<rt>しあい</rt></ruby>は<ruby>行<rt>おこな</rt></ruby>われます。", "<ruby>天候<rt>てんこう</rt></ruby>にかかわらずで、<ruby>試合<rt>しあい</rt></ruby>は<ruby>行<rt>おこな</rt></ruby>われます。"], "explanation": "'〜にかかわらず' means 'regardless of'."},
    {"question": "What does '〜つつある' imply?", "correct": "An action is currently in progress or changing.", "incorrect": ["An action was completed in the past.", "An action will never happen.", "An action is impossible to do."], "explanation": "'〜つつある' shows that a change is ongoing (e.g., 'improving', 'decreasing')."},
    {"question": "Translate: 'As soon as I arrived at the station, the train left.'", "correct": "<ruby>駅<rt>えき</rt></ruby>に<ruby>着<rt>つ</rt></ruby>いたとたん、<ruby>電車<rt>でんしゃ</rt></ruby>が<ruby>発車<rt>はっしゃ</rt></ruby>した。", "incorrect": ["<ruby>駅<rt>えき</rt></ruby>に<ruby>着<rt>つ</rt></ruby>くか<ruby>着<rt>つ</rt></ruby>かないうちに、<ruby>電車<rt>でんしゃ</rt></ruby>が<ruby>発車<rt>はっしゃ</rt></ruby>した。", "<ruby>駅<rt>えき</rt></ruby>に<ruby>着<rt>つ</rt></ruby>き<ruby>次第<rt>しだい</rt></ruby>、<ruby>電車<rt>でんしゃ</rt></ruby>が<ruby>発車<rt>はっしゃ</rt></ruby>した。", "<ruby>駅<rt>えき</rt></ruby>に<ruby>着<rt>つ</rt></ruby>いて<ruby>以来<rt>いらい</rt></ruby>、<ruby>電車<rt>でんしゃ</rt></ruby>が<ruby>発車<rt>はっしゃ</rt></ruby>した。"], "explanation": "'〜たとたん' means 'as soon as / the moment that' something happened."},
    {"question": "Which grammar point means 'from the standpoint of' or 'as'?", "correct": "〜として", "incorrect": ["〜にとって", "〜によって", "〜について"], "explanation": "'〜として' means 'in the capacity of' or 'as'."},
    {"question": "What does '〜にすぎない' mean?", "correct": "Nothing more than / Just", "incorrect": ["Too much", "Impossible", "Without a doubt"], "explanation": "'〜にすぎない' emphasizes that something is merely or only that thing."},
    {"question": "Translate: 'There is a fear/concern that prices will rise.'", "correct": "<ruby>物価<rt>ぶっか</rt></ruby>が<ruby>上<rt>あ</rt></ruby>がるおそれがある。", "incorrect": ["<ruby>物価<rt>ぶっか</rt></ruby>が<ruby>上<rt>あ</rt></ruby>がるはずがない。", "<ruby>物価<rt>ぶっか</rt></ruby>が<ruby>上<rt>あ</rt></ruby>がるわけがない。", "<ruby>物価<rt>ぶっか</rt></ruby>が<ruby>上<rt>あ</rt></ruby>がるどころではない。"], "explanation": "'〜おそれがある' means 'there is a fear/risk that...'."},
    {"question": "Translate: 'It is not necessarily true that expensive things are good.'", "correct": "<ruby>高<rt>たか</rt></ruby>いものがいいとは<ruby>限<rt>かぎ</rt></ruby>らない。", "incorrect": ["<ruby>高<rt>たか</rt></ruby>いものがいいに<ruby>違<rt>ちが</rt></ruby>いない。", "<ruby>高<rt>たか</rt></ruby>いものがいいはずがない。", "<ruby>高<rt>たか</rt></ruby>いものがいいわけがない。"], "explanation": "'〜とは<ruby>限<rt>かぎ</rt></ruby>らない' means 'not necessarily ~'."},
    {"question": "Translate: 'I can't possibly know that.'", "correct": "そんなこと、<ruby>知<rt>し</rt></ruby>るわけがない。", "incorrect": ["そんなこと、<ruby>知<rt>し</rt></ruby>るはずがある。", "そんなこと、<ruby>知<rt>し</rt></ruby>るに<ruby>違<rt>ちが</rt></ruby>いない。", "そんなこと、<ruby>知<rt>し</rt></ruby>るおそれがある。"], "explanation": "'〜わけがない' strongly denies a possibility ('there is no way')."},
    {"question": "What does '〜かねない' mean?", "correct": "There is a possibility of (something bad) happening.", "incorrect": ["Cannot possibly do.", "Must do.", "Have no choice but to do."], "explanation": "'〜かねない' is used when there's a risk of a negative outcome."},
    {"question": "Translate: 'While we are at it, let's clean the room.'", "correct": "ついでに、<ruby>部屋<rt>へや</rt></ruby>を<ruby>掃除<rt>そうじ</rt></ruby>しよう。", "incorrect": ["かわりに、<ruby>部屋<rt>へや</rt></ruby>を<ruby>掃除<rt>そうじ</rt></ruby>しよう。", "うえに、<ruby>部屋<rt>へや</rt></ruby>を<ruby>掃除<rt>そうじ</rt></ruby>しよう。", "くせに、<ruby>部屋<rt>へや</rt></ruby>を<ruby>掃除<rt>そうじ</rt></ruby>しよう。"], "explanation": "'〜ついでに' means 'while doing X, taking the opportunity to do Y'."},
    {"question": "What does '〜くせに' express?", "correct": "Criticism or blame (even though / despite).", "incorrect": ["Gratitude.", "Apology.", "Objective reason."], "explanation": "'〜くせに' implies reproach or dissatisfaction (e.g., 'Even though he knows nothing, he acts smart')."},
    {"question": "Choose the correct usage of '〜おかげで'.", "correct": "<ruby>先生<rt>せんせい</rt></ruby>のおかげで、<ruby>合格<rt>ごうかく</rt></ruby>できました。", "incorrect": ["<ruby>先生<rt>せんせい</rt></ruby>のせいで、<ruby>合格<rt>ごうかく</rt></ruby>できました。", "<ruby>先生<rt>せんせい</rt></ruby>の<ruby>代<rt>か</rt></ruby>わりに、<ruby>合格<rt>ごうかく</rt></ruby>できました。", "<ruby>先生<rt>せんせい</rt></ruby>のうえに、<ruby>合格<rt>ごうかく</rt></ruby>できました。"], "explanation": "'〜おかげで' is used to express gratitude for a positive result."},
    {"question": "Choose the correct usage of '〜せいで'.", "correct": "<ruby>雨<rt>あめ</rt></ruby>のせいで、<ruby>試合<rt>しあい</rt></ruby>が<ruby>中止<rt>ちゅうし</rt></ruby>になった。", "incorrect": ["<ruby>雨<rt>あめ</rt></ruby>のおかげで、<ruby>試合<rt>しあい</rt></ruby>が<ruby>中止<rt>ちゅうし</rt></ruby>になった。", "<ruby>雨<rt>あめ</rt></ruby>の<ruby>代<rt>か</rt></ruby>わりに、<ruby>試合<rt>しあい</rt></ruby>が<ruby>中止<rt>ちゅうし</rt></ruby>になった。", "<ruby>雨<rt>あめ</rt></ruby>のうえに、<ruby>試合<rt>しあい</rt></ruby>が<ruby>中止<rt>ちゅうし</rt></ruby>になった。"], "explanation": "'〜せいで' is used to blame something for a negative result."},
    {"question": "What does '〜をはじめ(として)' mean?", "correct": "Starting with / Representative example", "incorrect": ["At the very end", "Without", "Instead of"], "explanation": "'〜をはじめ' gives a primary example of a larger group."},
    {"question": "Translate: 'I read the book until the very end.'", "correct": "その<ruby>本<rt>ほん</rt></ruby>を<ruby>最後<rt>さいご</rt></ruby>まで<ruby>読<rt>よ</rt></ruby>み<ruby>抜<rt>ぬ</rt></ruby>いた。", "incorrect": ["その<ruby>本<rt>ほん</rt></ruby>を<ruby>最後<rt>さいご</rt></ruby>まで<ruby>読<rt>よ</rt></ruby>み<ruby>切<rt>き</rt></ruby>った。", "その<ruby>本<rt>ほん</rt></ruby>を<ruby>最後<rt>さいご</rt></ruby>まで<ruby>読<rt>よ</rt></ruby>みかけた。", "その<ruby>本<rt>ほん</rt></ruby>を<ruby>最後<rt>さいご</rt></ruby>まで<ruby>読<rt>よ</rt></ruby>み<ruby>直<rt>なお</rt></ruby>した。"], "explanation": "Both <ruby>読<rt>よ</rt></ruby>み<ruby>抜<rt>ぬ</rt></ruby>く and <ruby>読<rt>よ</rt></ruby>み<ruby>切<rt>き</rt></ruby>る can mean to read to the end, but '<ruby>抜<rt>ぬ</rt></ruby>く' emphasizes enduring a difficulty to the end."},
    {"question": "What does '〜からいうと' mean?", "correct": "From the perspective of / Judging from", "incorrect": ["Because of", "Since", "In order to"], "explanation": "'〜からいうと' means 'judging from the standpoint of'."}
]


all_questions = {
    "beginner": generate_questions("beginner", beg_vocab, beg_grammar),
    "intermediate": generate_questions("intermediate", int_vocab, int_grammar),
    "advanced": generate_questions("advanced", adv_vocab, adv_grammar)
}

js_content = f"const worksheetData = {json.dumps(all_questions, indent=2, ensure_ascii=False)};\n"

with open("/Users/mutahanaka/Desktop/日本語サイト/worksheet_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("worksheet_data.js generated successfully with 120 questions (now with furigana).")
