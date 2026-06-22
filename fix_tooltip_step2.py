import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replace_examples(m):
    step_id_str = m.group(1)
    step = int(step_id_str)
    
    if step != 2:
        return m.group(0)
        
    examples_str = m.group(3)
    try:
        examples = json.loads(examples_str)
        
        # Ex 0
        jp0 = examples[0]['jp']
        old_osaka = '<ruby>大阪<rt>おおさか</rt></ruby>'
        new_osaka = '<span class="tooltip-word" data-tooltip="Osaka" onclick="saveWordClick(this)"><ruby>大阪<rt>おおさか</rt></ruby></span>'
        
        if 'class="tooltip-word"' not in jp0.split(old_osaka)[0][-30:]:
            jp0 = jp0.replace(old_osaka, new_osaka)
        
        examples[0]['jp'] = jp0
        
        new_examples_str = json.dumps(examples, ensure_ascii=False)
        return m.group(0).replace(examples_str, new_examples_str)
    except json.JSONDecodeError as e:
        print("JSON Error", e)
        return m.group(0)

new_text = re.sub(r'pracStep(\d{2}): (\{.*?"examples": (\[.*?\]).*?"quizzes":)', replace_examples, text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Added tooltip to 大阪 in Step 2!")
