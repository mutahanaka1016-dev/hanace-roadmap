import csv
import os
import subprocess

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: "Hiragino Kaku Gothic Pro", "Hiragino Sans", sans-serif; padding: 20px; }}
        h1 {{ text-align: center; color: #ff751f; font-size: 24px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; page-break-inside: auto; }}
        tr {{ page-break-inside: avoid; page-break-after: auto; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #ff751f; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .kana {{ color: #666; font-size: 12px; }}
        .kanji {{ font-weight: bold; font-size: 16px; margin-bottom: 4px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <table>
        <thead>
            <tr>
                <th>Kanji</th>
                <th>Kana</th>
                <th>English</th>
                <th>Type</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""

def generate_html_from_csv(csv_filename, title):
    rows = []
    if not os.path.exists(csv_filename):
        print(f"File not found: {csv_filename}")
        return None
        
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kanji = row.get('Kanji', '')
            kana = row.get('Kana', '')
            eng = row.get('English', '')
            typ = row.get('Type', '')
            rows.append(f"<tr><td><div class='kanji'>{kanji}</div></td><td><div class='kana'>{kana}</div></td><td>{eng}</td><td>{typ}</td></tr>")
    
    return HTML_TEMPLATE.format(title=title, rows="\\n".join(rows))

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

files_to_process = [
    ('beginner_vocab.csv', 'beginner_vocab.pdf', 'Beginner Vocabulary List'),
    ('intermediate_vocab.csv', 'intermediate_vocab.pdf', 'Intermediate Vocabulary List'),
    ('practical_vocab.csv', 'practical_vocab.pdf', 'Practical Vocabulary List')
]

for csv_f, pdf_f, title in files_to_process:
    html_content = generate_html_from_csv(csv_f, title)
    if html_content:
        temp_html = csv_f.replace('.csv', '.html')
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Call Chrome headless
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_f}",
            temp_html
        ]
        
        subprocess.run(cmd, check=True)
        print(f"Generated {pdf_f}")
        os.remove(temp_html)
