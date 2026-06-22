import re
import json

def extract_steps(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will find all step keys like "step01:", "intStep01:", "pracStep01:"
    # and their vocabulary and examples blocks.
    
    # regex to match each step block roughly
    step_pattern = re.compile(r'(\b(?:step|intStep|pracStep)\d{2}\b)\s*:\s*\{(.*?)(?=\n\s*(?:step|intStep|pracStep)\d{2}\s*:|\n\s*};\n)', re.DOTALL)
    
    steps = {}
    for match in step_pattern.finditer(content):
        step_id = match.group(1)
        step_content = match.group(2)
        
        # extract vocab
        vocab_pattern = re.search(r'vocabulary\s*:\s*\[(.*?)\]\s*,', step_content, re.DOTALL)
        vocab_list = []
        if vocab_pattern:
            vocab_items = re.findall(r'\{\s*kana:\s*[\'"](.*?)[\'"]\s*,\s*kanji:\s*[\'"](.*?)[\'"]\s*,\s*romaji:\s*[\'"](.*?)[\'"]\s*,\s*meaning:\s*[\'"](.*?)[\'"]\s*\}', vocab_pattern.group(1))
            for item in vocab_items:
                vocab_list.append({
                    "kana": item[0],
                    "kanji": item[1],
                    "romaji": item[2],
                    "meaning": item[3]
                })
                
        # extract examples
        examples_pattern = re.search(r'examples\s*:\s*\[(.*?)\]', step_content, re.DOTALL)
        examples_list = []
        if examples_pattern:
            ex_items = re.findall(r'\{\s*jp:\s*[\'"](.*?)[\'"]\s*,\s*romaji:\s*[\'"](.*?)[\'"]\s*,\s*en:\s*[\'"](.*?)[\'"]\s*\}', examples_pattern.group(1))
            for item in ex_items:
                examples_list.append({
                    "jp": item[0],
                    "romaji": item[1],
                    "en": item[2]
                })
                
        steps[step_id] = {
            "vocabulary": vocab_list,
            "examples": examples_list
        }
        
    with open('step_data.json', 'w', encoding='utf-8') as f:
        json.dump(steps, f, ensure_ascii=False, indent=2)

extract_steps('index.html')
print("Extraction complete.")
