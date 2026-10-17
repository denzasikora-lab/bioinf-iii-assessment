"""Build the English laboratory notebook PDF from its Markdown source."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    PageBreak, Paragraph, SimpleDocTemplate, Spacer, XPreformatted)


ROOT = Path(__file__).resolve().parent
ACCENT = colors.HexColor('#234F68')


def inline(text):
    text = escape(text, quote=False)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',
                  r'<link href="\2" color="#234F68"><u>\1</u></link>', text)
    return re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)


def footer(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor('#CBD7DE'))
    canvas.line(48, 39, width - 48, 39)
    canvas.setFillColor(ACCENT)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(48, 26, 'BIOINF III | HBB sequence identification | English revision 14 October 2026')
    canvas.drawRightString(width - 48, 26, f'{document.page}')
    canvas.restoreState()


def main():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('ReportBody', fontName='Helvetica', fontSize=9.8,
                             leading=13.1, spaceAfter=7, alignment=TA_LEFT))
    styles.add(ParagraphStyle('ReportTitle', fontName='Helvetica-Bold', fontSize=25,
                             leading=29, textColor=ACCENT, spaceAfter=13))
    styles.add(ParagraphStyle('ReportHeading', fontName='Helvetica-Bold', fontSize=13,
                             leading=17, textColor=ACCENT, spaceBefore=8,
                             spaceAfter=8, keepWithNext=True))
    styles.add(ParagraphStyle('ReportCode', fontName='Courier', fontSize=7.7,
                             leading=10.2, leftIndent=9, rightIndent=9,
                             borderPadding=7, backColor=colors.HexColor('#EFF4F7'),
                             spaceBefore=4, spaceAfter=9))
    styles.add(ParagraphStyle('ReportQuote', parent=styles['ReportBody'],
                             fontName='Helvetica-Oblique', leftIndent=13,
                             rightIndent=13, textColor=ACCENT, spaceBefore=4))
    story = []
    paragraph = []
    code_lines = []
    in_code = False

    def flush_paragraph():
        if paragraph:
            story.append(Paragraph(inline(' '.join(paragraph)), styles['ReportBody']))
            paragraph.clear()

    for line in (ROOT / 'HBB_sequence_report.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('```'):
            flush_paragraph()
            if in_code:
                story.append(XPreformatted(escape('\n'.join(code_lines)), styles['ReportCode']))
                code_lines.clear()
            in_code = not in_code
        elif in_code:
            code_lines.append(line)
        elif line == '<!-- pagebreak -->':
            flush_paragraph()
            story.append(PageBreak())
        elif line.startswith('# '):
            flush_paragraph()
            story.append(Paragraph(inline(line[2:]), styles['ReportTitle']))
        elif line.startswith('## '):
            flush_paragraph()
            story.append(Paragraph(inline(line[3:]), styles['ReportHeading']))
        elif line.startswith('> '):
            flush_paragraph()
            story.append(Paragraph(inline(line[2:]), styles['ReportQuote']))
        elif line.startswith('* '):
            flush_paragraph()
            story.append(Paragraph(inline(line[2:]), styles['ReportBody'], bulletText='-'))
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line.strip())
    flush_paragraph()
    if in_code:
        raise ValueError('Unclosed code block in the report source')
    document = SimpleDocTemplate(str(ROOT / 'HBB_sequence_report.pdf'), pagesize=A4,
        rightMargin=48, leftMargin=48, topMargin=43, bottomMargin=50,
        title='HBB sequence identification: laboratory notebook', author='Egor Fedosov')
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print('Built:', ROOT / 'HBB_sequence_report.pdf')


if __name__ == '__main__':
    main()
