import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replace_examples(m):
    step_id_str = m.group(1)
    step = int(step_id_str)
    
    if step != 5:
        return m.group(0)
        
    examples_str = m.group(3)
    try:
        examples = json.loads(examples_str)
        
        # Ex 2
        jp2 = examples[2]['jp']
        new_shikamo = '<span class="tooltip-word" data-tooltip="what\'s more / moreover" onclick="saveWordClick(this)">しかも</span>'
        # Only replace if not already replaced
        if 'class="tooltip-word"' not in jp2.split('しかも')[0][-30:]:
            jp2 = jp2.replace("しかも", new_shikamo)
        
        examples[2]['jp'] = jp2
        
        new_examples_str = json.dumps(examples, ensure_ascii=False)
        return m.group(0).replace(examples_str, new_examples_str)
    except json.JSONDecodeError as e:
        print("JSON Error", e)
        return m.group(0)

new_text = re.sub(r'pracStep(\d{2}): (\{.*?"examples": (\[.*?\]).*?"quizzes":)', replace_examples, text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Added tooltip to しかも in Step 5!")
