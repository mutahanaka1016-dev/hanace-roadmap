import json
import re

with open('annotated_sentences.json', 'r', encoding='utf-8') as f:
    annotations = json.load(f)

# Find all text outside of the span tags.
# Since the format is <span ...>WORD</span>, we can split by spans.
# We just need to remove all spans and ruby tags, and see what's left.

def extract_unannotated_text(annotated_str):
    # Remove the contents of the spans
    # Wait, if we remove the spans AND their contents, we are left with the unannotated text.
    # The span structure is: <span class="tooltip-word" data-tooltip="... " onclick="...">...</span>
    text_outside_spans = re.sub(r'<span class="tooltip-word".*?>.*?</span>', ' ', annotated_str)
    
    # Also clean up ruby tags if they somehow leaked (though they shouldn't if they were annotated)
    text_outside_spans = re.sub(r'<rt>.*?</rt>', '', text_outside_spans)
    text_outside_spans = text_outside_spans.replace('<ruby>', '').replace('</ruby>', '')
    
    # Remove particles, punctuation, spaces
    # Common particles: は, が, を, に, で, と, も, から, まで, の, か, ね, よ, て, ば, な, ーー, 、, 。
    particles = ['は', 'が', 'を', 'に', 'で', 'と', 'も', 'から', 'まで', 'の', 'か', 'ね', 'よ', 'て', 'ば', 'な', 'ーー', '、', '。', '？', '！', ' ', '　', 'です', 'でした', 'ます', 'ました', 'ではありません', 'じゃありません', 'じゃない', 'ません', 'って', 'なので', 'だから']
    
    for p in particles:
        text_outside_spans = text_outside_spans.replace(p, ' ')
        
    return " ".join(text_outside_spans.split())

missing = set()
for jp, annotated in annotations.items():
    unannotated = extract_unannotated_text(annotated)
    if unannotated.strip():
        # Let's see the context
        print(f"Original: {jp}")
        print(f"Annotated: {annotated}")
        print(f"Missing text roughly: {unannotated}")
        print("-" * 40)
        missing.update(unannotated.split())
        
print("Potentially missing words/chunks:")
print(missing)
