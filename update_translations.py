import json
import re

translations = {
    1: [
        "I chose this movie.",
        "I eat sashimi, but I don't eat meat.",
        "I think Japanese is difficult.",
        "Actually, my wallet was found! It was at the station's police box."
    ],
    2: [
        "Food in Tokyo is not as delicious as in Osaka.",
        "Mr. Tanaka is the smartest in this class.",
        "The more you study, the better your Japanese will become.",
        "The more convenient things become, the lazier humans get."
    ],
    3: [
        "I can speak Japanese.",
        "I can play the piano.",
        "Before going to Japan, I couldn't speak Japanese.",
        "Can you eat natto?"
    ],
    4: [
        "If you turn right, there is a post office.",
        "If I had money, I would want to travel.",
        "If you go to Japan, you definitely should go to Kyoto.",
        "If you write a diary in Japanese every day, you will definitely get better at it!"
    ],
    5: [
        "The train was delayed. Because of that, I was late for the meeting.",
        "I think this plan is good. However, we don't have enough budget.",
        "This apartment is close to the station. Moreover, it's cheap!",
        "Japanese is difficult. However, it is very fun. Furthermore, the more you study, the better you become. Therefore, I never miss my daily practice."
    ],
    6: [
        "Thank you for going out of your way to come here.",
        "The window has been left open (intentionally).",
        "I booked the hotel in advance of the trip.",
        "I accidentally ate the whole cake (or completely finished it)."
    ],
    7: [
        "My teacher gave me advice.",
        "I received advice from my teacher.",
        "I humbly received advice from my teacher.",
        "I'm moving next time, could you help me?"
    ],
    8: [
        "The toy broke.",
        "I broke the toy.",
        "The window has been opened (intentionally).",
        "The window is open."
    ],
    9: [
        "It looks like it's going to rain.",
        "I heard that the company is relocating next year.",
        "It seems she is getting married next week.",
        "I tried contacting their phone, but couldn't get through; it seems they caught a cold."
    ],
    10: [
        "I had my cake eaten by my friend.",
        "Please let me think about it a little more.",
        "When I was a child, I was forced to practice the piano every day.",
        "Actually, I regrettably had something terrible said to me by my boss."
    ],
    11: [
        "I will carry it for you.",
        "May I ask your name?",
        "Thank you for your continued support (standard business greeting).",
        "Could you please submit the report by next week?"
    ],
    12: [
        "Regrettably, the machine broke...",
        "Because my boss made me work overtime, my reply was delayed.",
        "The reservation has been made in advance.",
        "I took a backup in advance."
    ],
    13: [
        "I think that the more technology advances, the more human jobs will decrease.",
        "If everyone in the world could speak Japanese, cultural exchange would likely become more active.",
        "I think that SNS has a negative influence on young people.",
        "Compared to my country, I think public transportation is more developed in Japan."
    ]
}

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replace_examples(m):
    step_id_str = m.group(1)
    step = int(step_id_str)
    
    if step > 13:
        return m.group(0)
        
    examples_str = m.group(2)
    try:
        examples = json.loads(examples_str)
        if step in translations:
            trans_list = translations[step]
            for i, ex in enumerate(examples):
                if i < len(trans_list):
                    ex['en'] = trans_list[i]
        
        new_examples_str = json.dumps(examples, ensure_ascii=False)
        # Using string replacement just in case regex captured groups loosely
        return m.group(0).replace(examples_str, new_examples_str)
    except json.JSONDecodeError:
        return m.group(0)

# The regex should capture the "examples": [ ... ] block inside pracStepXX
# Be careful with the regex to match up to "quizzes":
new_text = re.sub(r'pracStep(\d{2}): (\{.*?"examples": (\[.*?\])(?=, "quizzes":))', replace_examples, text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated translations in index.html!")
