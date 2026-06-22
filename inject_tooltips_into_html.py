import json
import re

with open('annotated_sentences.json', 'r', encoding='utf-8') as f:
    annotations = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    quote = "'" if match.group(1) is not None else '"'
    jp_text = match.group(1) if match.group(1) is not None else match.group(2)
    
    # Strip span tags from jp_text in case they were injected previously
    raw_jp_text = re.sub(r'<span class=\\?"tooltip-word\\?".*?>', '', jp_text)
    raw_jp_text = raw_jp_text.replace('</span>', '')
    
    # Normalize escaped quotes for key matching
    key_text = raw_jp_text.replace(r'\"', '"').replace(r"\'", "'")
    
    if key_text in annotations and annotations[key_text]:
        new_text = annotations[key_text]
        # Escape quotes matching the outer quote type
        if quote == "'":
            new_text = new_text.replace("'", "\\'")
        elif quote == '"':
            new_text = new_text.replace('"', '\\"')
        
        # Preserve original prefix style ("jp" vs jp)
        full_match = match.group(0)
        prefix = '"jp"' if full_match.startswith('"') else 'jp'
        return f"{prefix}: {quote}{new_text}{quote}"
    
    return match.group(0)

# Regex to match jp: '...' or jp: "..." with escaped quotes support
pattern = re.compile(r'(?:"jp"|jp)\s*:\s*(?:\'((?:[^\'\\]|\\.)*)\'|"((?:[^"\\]|\\.)*)")')
new_content = pattern.sub(replacer, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Injected tooltips into index.html successfully.")
