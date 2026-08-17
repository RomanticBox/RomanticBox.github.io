#!/usr/bin/env python3
"""
CV PDF Generator
Generates a professional CV PDF from resume.json file
"""

import json
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_WIDTH = 7.0 * inch  # usable width after 0.75in margins on letter size

def load_resume_data(json_path):
    """Load resume data from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def strip_unrenderable_glyphs(text):
    """Strip Hangul parentheticals and flag emoji: reportlab's base fonts (Helvetica)
    have no Hangul glyphs and no color-emoji support, so they render as blank boxes."""
    text = re.sub(r'\s*\([^)]*[가-힣][^)]*\)', '', text)
    text = re.sub(r'[\U0001F1E6-\U0001F1FF]', '', text)
    return re.sub(r'\s{2,}', ' ', text).strip()

def format_date(date_str):
    """Format date string (YYYY-MM-DD) to readable format"""
    if not date_str or date_str == "":
        return "Present"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %Y")
    except:
        return date_str

def to_bullets(text):
    """Split a summary paragraph into standalone sentences for bullet display."""
    if not text:
        return []
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]

def sorted_by_date(entries, key='startDate', reverse=True):
    return sorted(entries, key=lambda e: e.get(key) or '', reverse=reverse)

def create_cv_pdf(resume_data, output_path, base_dir):
    """Create CV PDF from resume data"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch,
        title="CV(Sunghyun Lee, KAIST)",
        author="Sunghyun Lee",
        subject="Curriculum Vitae",
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'], fontSize=22,
        textColor=colors.HexColor('#1a1a1a'), spaceAfter=2, alignment=TA_LEFT
    )
    label_style = ParagraphStyle(
        'CustomLabel', parent=styles['Normal'], fontSize=11,
        textColor=colors.HexColor('#2c5aa0'), spaceAfter=4
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'], fontSize=13,
        textColor=colors.white, backColor=colors.HexColor('#2c3e50'),
        spaceAfter=8, spaceBefore=14, fontName='Helvetica-Bold',
        leftIndent=6, borderPadding=(4, 4, 4, 4)
    )
    normal_style = ParagraphStyle(
        'CustomNormal', parent=styles['Normal'], fontSize=9.5,
        textColor=colors.HexColor('#333333'), leading=13
    )
    bold_style = ParagraphStyle('CustomBold', parent=normal_style, fontName='Helvetica-Bold')
    small_italic_style = ParagraphStyle(
        'CustomSmallItalic', parent=normal_style, fontSize=9,
        textColor=colors.HexColor('#555555'), fontName='Helvetica-Oblique'
    )
    bullet_style = ParagraphStyle('CustomBullet', parent=normal_style, leftIndent=10, spaceAfter=2)

    def cell_para(text, style=normal_style):
        return Paragraph(text, style)

    def section_heading(text):
        story.append(Paragraph(text.upper(), heading_style))

    def styled_table(rows, col_widths, header=False):
        table = Table(rows, colWidths=col_widths, hAlign='LEFT')
        cmds = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]
        start = 0
        if header:
            cmds.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eef1f5')))
            start = 1
        for i in range(start, len(rows)):
            if (i - start) % 2 == 1:
                cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f7f7f9')))
        table.setStyle(TableStyle(cmds))
        story.append(table)
        story.append(Spacer(1, 0.15*inch))

    # ------------------------------------------------------------------
    # Header: photo + name + contact + links
    # ------------------------------------------------------------------
    basics = resume_data.get('basics', {})
    name = strip_unrenderable_glyphs(basics.get('name', ''))
    label = basics.get('label', '')
    email = basics.get('email', '')
    url = basics.get('url', '')
    nationality = strip_unrenderable_glyphs(basics.get('nationality', ''))
    summary = basics.get('summary', '')
    location = basics.get('location', {})
    profiles = basics.get('profiles', [])

    contact_info = []
    if email:
        contact_info.append(f"Email: {email}")
    if nationality:
        contact_info.append(f"Nationality: {nationality}")
    if location.get('city') and location.get('countryCode'):
        contact_info.append(f"Location: {location['city']}, {location['countryCode']}")

    link_parts = []
    if url:
        link_parts.append(f'<link href="{url}" color="#2c5aa0">Website</link>')
    for profile in profiles:
        network = profile.get('network', '')
        profile_url = profile.get('url', '')
        username = profile.get('username', '')
        if profile_url:
            link_parts.append(f'<link href="{profile_url}" color="#2c5aa0">{network}</link>')
        elif network and username:
            link_parts.append(f"{network}: {username}")

    header_right = [Paragraph(name, title_style)]
    if label:
        header_right.append(Paragraph(label, label_style))
    if contact_info:
        header_right.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_info), normal_style))
    if link_parts:
        header_right.append(Paragraph(" &nbsp;|&nbsp; ".join(link_parts), normal_style))

    photo_path = os.path.join(base_dir, 'assets', 'img', 'prof_pic.jpg')
    if os.path.exists(photo_path):
        photo_width = 1.1 * inch
        photo_height = photo_width * (4032 / 3024)
        header_left = Image(photo_path, width=photo_width, height=photo_height)
        header_table = Table(
            [[header_left, header_right]],
            colWidths=[1.3*inch, PAGE_WIDTH - 1.3*inch],
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 12),
        ]))
        story.append(header_table)
    else:
        story.extend(header_right)
    story.append(Spacer(1, 0.15*inch))

    # Summary as bullet points
    summary_bullets = to_bullets(summary)
    if summary_bullets:
        section_heading('Summary')
        for b in summary_bullets:
            story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(1, 0.1*inch))

    # ------------------------------------------------------------------
    # Education (most important for an academic CV)
    # ------------------------------------------------------------------
    education = sorted_by_date(resume_data.get('education', []))
    if education:
        section_heading('Education')
        rows = [[cell_para('<b>Degree</b>'), cell_para('<b>Period</b>'), cell_para('<b>GPA</b>')]]
        for edu in education:
            degree_lines = f"<b>{edu.get('studyType', '')} in {edu.get('area', '')}</b><br/>{edu.get('institution', '')}"
            period = f"{format_date(edu.get('startDate', ''))} – {format_date(edu.get('endDate', ''))}"
            score = edu.get('score', '') or '—'
            rows.append([cell_para(degree_lines), cell_para(period), cell_para(score)])
        styled_table(rows, [3.8*inch, 1.9*inch, 1.3*inch], header=True)

    # ------------------------------------------------------------------
    # Publications
    # ------------------------------------------------------------------
    publications = sorted_by_date(resume_data.get('publications', []), key='releaseDate')
    if publications:
        section_heading('Publications')
        rows = []
        for pub in publications:
            authors = pub.get('authors', '').replace('Sunghyun Lee', '<b>Sunghyun Lee</b>')
            block = f"<b>{pub.get('name', '')}</b><br/>{pub.get('publisher', '')} ({format_date(pub.get('releaseDate', ''))})"
            if authors:
                block += f"<br/>{authors}"
            if pub.get('summary'):
                block += f"<br/><i>{pub['summary']}</i>"
            rows.append([cell_para(block)])
        styled_table(rows, [PAGE_WIDTH])

    # ------------------------------------------------------------------
    # Work Experience
    # ------------------------------------------------------------------
    work = sorted_by_date(resume_data.get('work', []))
    if work:
        section_heading('Work Experience')
        rows = []
        for job in work:
            position = job.get('position', '').replace('**', '')
            block = f"<b>{job.get('name', '')}</b>"
            if position:
                block += f" — {position}"
            if job.get('summary'):
                block += f"<br/>{job['summary']}"
            highlights = [h for h in job.get('highlights', []) if h and h.strip()]
            for h in highlights:
                block += f"<br/>• {h}"
            period = f"{format_date(job.get('startDate', ''))} –<br/>{format_date(job.get('endDate', ''))}"
            rows.append([cell_para(block), cell_para(period)])
        styled_table(rows, [PAGE_WIDTH - 1.4*inch, 1.4*inch])

    # ------------------------------------------------------------------
    # Awards
    # ------------------------------------------------------------------
    awards = sorted_by_date(resume_data.get('awards', []), key='date')
    if awards:
        section_heading('Awards & Honors')
        rows = [[cell_para('<b>Award</b>'), cell_para('<b>Awarder</b>'), cell_para('<b>Date</b>')]]
        for award in awards:
            title_block = award.get('title', '')
            if award.get('summary'):
                title_block += f"<br/><i>{award['summary']}</i>"
            rows.append([cell_para(title_block), cell_para(award.get('awarder', '')), cell_para(format_date(award.get('date', '')))])
        styled_table(rows, [4.0*inch, 1.7*inch, 1.3*inch], header=True)

    # ------------------------------------------------------------------
    # Skills
    # ------------------------------------------------------------------
    skills = resume_data.get('skills', [])
    if skills:
        section_heading('Skills')
        rows = []
        for skill in skills:
            keywords = ', '.join(skill.get('keywords', []))
            rows.append([cell_para(f"<b>{skill.get('name', '')}</b>"), cell_para(keywords)])
        styled_table(rows, [1.6*inch, PAGE_WIDTH - 1.6*inch])

    # ------------------------------------------------------------------
    # Languages
    # ------------------------------------------------------------------
    languages = resume_data.get('languages', [])
    if languages:
        section_heading('Languages')
        rows = []
        for lang in languages:
            if lang.get('language') and lang.get('fluency'):
                rows.append([cell_para(f"<b>{lang['language']}</b>"), cell_para(lang['fluency'])])
        if rows:
            styled_table(rows, [1.6*inch, PAGE_WIDTH - 1.6*inch])

    # ------------------------------------------------------------------
    # Certificates
    # ------------------------------------------------------------------
    certificates = [c for c in resume_data.get('certificates', []) if c.get('name') and c.get('name').strip()]
    if certificates:
        section_heading('Certificates')
        rows = [[cell_para('<b>Certificate</b>'), cell_para('<b>Issuer</b>'), cell_para('<b>Date</b>')]]
        for cert in certificates:
            rows.append([cell_para(cert.get('name', '')), cell_para(cert.get('issuer', '')), cell_para(format_date(cert.get('date', '')))])
        styled_table(rows, [4.0*inch, 1.7*inch, 1.3*inch], header=True)

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------
    projects = sorted_by_date(resume_data.get('projects', []))
    if projects:
        section_heading('Projects')
        rows = []
        for project in projects:
            block = f"<b>{project.get('name', '')}</b>"
            if project.get('summary'):
                block += f"<br/>{project['summary']}"
            for h in [h for h in project.get('highlights', []) if h and h.strip()]:
                block += f"<br/>• {h}"
            period = f"{format_date(project.get('startDate', ''))} –<br/>{format_date(project.get('endDate', ''))}"
            rows.append([cell_para(block), cell_para(period)])
        styled_table(rows, [PAGE_WIDTH - 1.4*inch, 1.4*inch])

    # Build PDF
    doc.build(story)
    print(f"CV PDF successfully generated: {output_path}")

def main():
    """Main function"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'assets', 'json', 'resume.json')
    output_path = os.path.join(script_dir, 'assets', 'pdf', 'cv.pdf')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load resume data
    resume_data = load_resume_data(json_path)

    # Generate PDF
    create_cv_pdf(resume_data, output_path, script_dir)

if __name__ == '__main__':
    main()
