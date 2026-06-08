import csv
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a Japanese font
font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"
if not os.path.exists(font_path):
    print(f"Font not found: {font_path}")
    # try another
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    if not os.path.exists(font_path):
        print(f"Font not found: {font_path}")

try:
    pdfmetrics.registerFont(TTFont('Hiragino', font_path, subfontIndex=0))
except Exception as e:
    print(f"Error registering font: {e}")

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontName='Hiragino',
    fontSize=18,
    alignment=1, # Center
    spaceAfter=20
)
normal_style = ParagraphStyle(
    'NormalStyle',
    parent=styles['Normal'],
    fontName='Hiragino',
    fontSize=10,
)

def csv_to_pdf(csv_filename, pdf_filename, title):
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []
    
    # Add title
    elements.append(Paragraph(title, title_style))
    
    # Read CSV
    data = []
    headers = ["Kanji", "Kana", "English", "Type"]
    data.append(headers)
    
    try:
        with open(csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append([
                    Paragraph(row.get('Kanji', ''), normal_style),
                    Paragraph(row.get('Kana', ''), normal_style),
                    Paragraph(row.get('English', ''), normal_style),
                    Paragraph(row.get('Type', ''), normal_style)
                ])
    except Exception as e:
        print(f"Error reading {csv_filename}: {e}")
        return

    # Create table
    col_widths = [100, 100, 180, 100]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    
    # Table style
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#ff751f")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Hiragino'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    print(f"Successfully created {pdf_filename}")

files_to_process = [
    ('beginner_vocab.csv', 'beginner_vocab.pdf', 'Beginner Vocabulary List'),
    ('intermediate_vocab.csv', 'intermediate_vocab.pdf', 'Intermediate Vocabulary List'),
    ('practical_vocab.csv', 'practical_vocab.pdf', 'Practical Vocabulary List')
]

for csv_f, pdf_f, title in files_to_process:
    if os.path.exists(csv_f):
        csv_to_pdf(csv_f, pdf_f, title)
    else:
        print(f"CSV file not found: {csv_f}")
