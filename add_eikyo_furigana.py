import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Put the furigana back
new_text = text.replace("悪い影響を", "悪い<ruby>影響<rt>えいきょう</rt></ruby>を")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Successfully put furigana back for 影響")
