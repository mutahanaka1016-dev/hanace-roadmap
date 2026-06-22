import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replace_examples(m):
    step_id_str = m.group(1)
    step = int(step_id_str)
    
    if step != 9:
        return m.group(0)
        
    examples_str = m.group(3)
    try:
        examples = json.loads(examples_str)
        
        # Ex 2
        jp2 = examples[2]['jp']
        jp2 = jp2.replace("<ruby>彼女<rt>かのじょ</rt></ruby>", '<span class="tooltip-word" data-tooltip="she / girlfriend" onclick="saveWordClick(this)"><ruby>彼女<rt>かのじょ</rt></ruby></span>')
        jp2 = jp2.replace("<ruby>来週<rt>らいしゅう</rt></ruby>", '<span class="tooltip-word" data-tooltip="next week" onclick="saveWordClick(this)"><ruby>来週<rt>らいしゅう</rt></ruby></span>')
        examples[2]['jp'] = jp2

        # Ex 3
        jp3 = examples[3]['jp']
        # Currently: <ruby>携帯<rt>けいたい</rt></ruby>に<ruby>連絡<rt>れんらく</rt></ruby><span class="tooltip-word" data-tooltip="did" onclick="saveWordClick(this)">した</span>んですが、
        # We want to replace `<ruby>連絡<rt>れんらく</rt></ruby><span class="tooltip-word" data-tooltip="did" onclick="saveWordClick(this)">した</span>`
        # with a single tooltip.
        old_renraku_shita = '<ruby>連絡<rt>れんらく</rt></ruby><span class="tooltip-word" data-tooltip="did" onclick="saveWordClick(this)">した</span>'
        new_renraku_shita = '<span class="tooltip-word" data-tooltip="contacted" onclick="saveWordClick(this)"><ruby>連絡<rt>れんらく</rt></ruby>した</span>'
        
        if old_renraku_shita in jp3:
            jp3 = jp3.replace(old_renraku_shita, new_renraku_shita)
        else:
            # Maybe it doesn't have the tooltip on した, just wrap 連絡した
            # Let's just do a regex replace to be safe
            jp3 = re.sub(r'<ruby>連絡<rt>れんらく</rt></ruby>(<span.*?>)?した(</span>)?', new_renraku_shita, jp3)
            
        examples[3]['jp'] = jp3
        
        new_examples_str = json.dumps(examples, ensure_ascii=False)
        return m.group(0).replace(examples_str, new_examples_str)
    except json.JSONDecodeError as e:
        print("JSON Error", e)
        return m.group(0)

new_text = re.sub(r'pracStep(\d{2}): (\{.*?"examples": (\[.*?\]).*?"quizzes":)', replace_examples, text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Added tooltips to Step 9!")
