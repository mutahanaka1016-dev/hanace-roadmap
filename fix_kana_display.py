import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

target = "${word.kanji ? '(' + word.kana + ')' : ''}"
replacement = "${(word.kanji && word.kanji !== word.kana) ? '(' + word.kana + ')' : ''}"

new_text = text.replace(target, replacement)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Successfully updated kana display logic in index.html")
