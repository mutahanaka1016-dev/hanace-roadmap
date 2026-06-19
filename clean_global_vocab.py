import re
import json

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# We want to find the GLOBAL_VOCAB block and filter its keys.
# Let's extract the block.
start_idx = text.find("const GLOBAL_VOCAB = {")
if start_idx == -1:
    print("GLOBAL_VOCAB not found")
    exit(1)

# Find the closing brace of GLOBAL_VOCAB
# It ends when we see "};" or similar at the same indentation, but let's just find the closing brace by counting.
end_idx = text.find("        for (let word in GLOBAL_VOCAB) {", start_idx)

vocab_block = text[start_idx:end_idx]

# Split into lines
lines = vocab_block.split("\n")
new_lines = []

def is_valid_key(line):
    # match `"key": "value",`
    m = re.search(r'^\s*"([^"]+)":', line)
    if not m:
        return True # Not a vocab line, maybe a comment or the opening brace
        
    key = m.group(1)
    
    # If it contains < or >
    if "<" in key or ">" in key:
        # It must start with <ruby> and end with </ruby> and have perfectly balanced tags inside?
        # A simple check: if it doesn't end with </ruby>, it's bad.
        if not key.endswith("</ruby>"):
            return False
        # If it doesn't start with <ruby>, it's bad.
        if not key.startswith("<ruby>"):
            return False
        # If it has <ruby> anywhere except the start, it's bad.
        if key.count("<ruby>") > 1:
            return False
            
    return True

deleted_count = 0
for line in lines:
    if is_valid_key(line):
        new_lines.append(line)
    else:
        deleted_count += 1
        print("Deleted:", line.strip())

new_vocab_block = "\n".join(new_lines)

# Now, also I should remove my 176 injected items if the user wanted a full revert.
# But wait, my 176 items are perfectly valid `<ruby>...<rt>...</rt></ruby>`!
# They fix the popup boundaries. They don't break the DOM.
# The broken DOM was from the `りんご<ruby>` and `<ruby>少<rt>すこ</rt></ruby>し<ruby>`.
# So deleting the malformed tags will fix the DOM!

new_text = text[:start_idx] + new_vocab_block + text[end_idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print(f"Successfully cleaned GLOBAL_VOCAB. Deleted {deleted_count} malformed entries.")
