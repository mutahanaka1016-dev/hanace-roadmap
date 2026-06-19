import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the kanji/furigana layout
text = text.replace("<ruby>考<rt>かんが</rt></ruby>えます", "<ruby>考<rt>かん</rt></ruby>がえます")

# Also add the new ruby-tagged string to GLOBAL_VOCAB so the popup still works
vocab_add = '            "<ruby>考<rt>かん</rt></ruby>がえます": "[V] Think",\n'
pattern_global = r"(const GLOBAL_VOCAB = \{)"

def repl(m):
    return m.group(1) + "\n" + vocab_add

text, count = re.subn(pattern_global, repl, text, count=1)

if count > 0:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully replaced and added to GLOBAL_VOCAB.")
else:
    print("Failed to find GLOBAL_VOCAB.")
