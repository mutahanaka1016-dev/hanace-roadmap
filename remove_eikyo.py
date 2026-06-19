import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Replace specifically the phrase in the sentence
new_text = text.replace("<ruby>影響<rt>えいきょう</rt></ruby>を", "影響を")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Successfully removed furigana for 影響")
