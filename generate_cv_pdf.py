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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

def create_cv_pdf(resume_data, output_path):
    """Create CV PDF from resume data"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        leading=14
    )
    
    # Header: Name and Contact Info
    basics = resume_data.get('basics', {})
    name = strip_unrenderable_glyphs(basics.get('name', ''))
    label = basics.get('label', '')
    email = basics.get('email', '')
    url = basics.get('url', '')
    nationality = strip_unrenderable_glyphs(basics.get('nationality', ''))
    summary = basics.get('summary', '')
    location = basics.get('location', {})
    
    story.append(Paragraph(name, title_style))
    if label:
        story.append(Paragraph(label, normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Contact information
    contact_info = []
    if email:
        contact_info.append(f"Email: {email}")
    if nationality:
        contact_info.append(f"Nationality: {nationality}")
    if url:
        contact_info.append(f"Website: {url}")
    if location.get('city') and location.get('countryCode'):
        contact_info.append(f"Location: {location['city']}, {location['countryCode']}")
    
    if contact_info:
        story.append(Paragraph(" | ".join(contact_info), normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Social profiles
    profiles = basics.get('profiles', [])
    if profiles:
        profile_links = []
        for profile in profiles:
            network = profile.get('network', '')
            username = profile.get('username', '')
            if network and username:
                profile_links.append(f"{network}: {username}")
        if profile_links:
            story.append(Paragraph(" | ".join(profile_links), normal_style))
            story.append(Spacer(1, 0.15*inch))
    
    # Summary
    if summary:
        story.append(Paragraph("<b>Summary</b>", heading_style))
        story.append(Paragraph(summary, normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Education
    education = resume_data.get('education', [])
    if education:
        story.append(Paragraph("<b>Education</b>", heading_style))
        for edu in education:
            institution = edu.get('institution', '')
            area = edu.get('area', '')
            study_type = edu.get('studyType', '')
            start_date = format_date(edu.get('startDate', ''))
            end_date = format_date(edu.get('endDate', ''))
            score = edu.get('score', '')
            
            edu_text = f"<b>{institution}</b>"
            if area:
                edu_text += f"<br/>{area}"
            if study_type:
                edu_text += f"<br/>{study_type}"
            if start_date and end_date:
                edu_text += f"<br/>{start_date} - {end_date}"
            if score:
                edu_text += f" | GPA: {score}"
            
            story.append(Paragraph(edu_text, normal_style))
            story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Work Experience
    work = resume_data.get('work', [])
    if work:
        story.append(Paragraph("<b>Work Experience</b>", heading_style))
        for job in work:
            name = job.get('name', '')
            position = job.get('position', '').replace('**', '')
            start_date = format_date(job.get('startDate', ''))
            end_date = format_date(job.get('endDate', ''))
            summary = job.get('summary', '')
            highlights = job.get('highlights', [])

            work_text = f"<b>{name}</b>"
            if position:
                work_text += f" | {position}"
            if start_date and end_date:
                work_text += f"<br/>{start_date} - {end_date}"
            elif start_date:
                work_text += f"<br/>{start_date} - Present"
            
            story.append(Paragraph(work_text, normal_style))
            if summary:
                story.append(Paragraph(summary, normal_style))
            if highlights:
                for highlight in highlights:
                    if highlight and highlight.strip():
                        story.append(Paragraph(f"• {highlight}", normal_style))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Publications
    publications = resume_data.get('publications', [])
    if publications:
        story.append(Paragraph("<b>Publications</b>", heading_style))
        for pub in publications:
            name = pub.get('name', '')
            publisher = pub.get('publisher', '')
            release_date = format_date(pub.get('releaseDate', ''))
            summary = pub.get('summary', '')
            authors = pub.get('authors', '').replace('Sunghyun Lee', '<b>Sunghyun Lee</b>')
            url = pub.get('url', '')

            pub_text = f"<b>{name}</b>"
            if publisher:
                pub_text += f" | {publisher}"
            if release_date:
                pub_text += f" ({release_date})"
            if authors:
                pub_text += f"<br/>{authors}"
            if summary:
                pub_text += f"<br/>{summary}"
            
            story.append(Paragraph(pub_text, normal_style))
            story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Projects
    projects = resume_data.get('projects', [])
    if projects:
        story.append(Paragraph("<b>Projects</b>", heading_style))
        for project in projects:
            name = project.get('name', '')
            summary = project.get('summary', '')
            start_date = format_date(project.get('startDate', ''))
            end_date = format_date(project.get('endDate', ''))
            highlights = project.get('highlights', [])
            
            proj_text = f"<b>{name}</b>"
            if start_date and end_date:
                proj_text += f" ({start_date} - {end_date})"
            elif start_date:
                proj_text += f" ({start_date} - Present)"
            
            story.append(Paragraph(proj_text, normal_style))
            if summary:
                story.append(Paragraph(summary, normal_style))
            if highlights:
                for highlight in highlights:
                    if highlight and highlight.strip():
                        story.append(Paragraph(f"• {highlight}", normal_style))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Awards
    awards = resume_data.get('awards', [])
    if awards:
        story.append(Paragraph("<b>Awards</b>", heading_style))
        for award in awards:
            title = award.get('title', '')
            date = format_date(award.get('date', ''))
            awarder = award.get('awarder', '')
            summary = award.get('summary', '')
            
            award_text = f"<b>{title}</b>"
            if awarder:
                award_text += f" | {awarder}"
            if date:
                award_text += f" ({date})"
            if summary:
                award_text += f"<br/>{summary}"
            
            story.append(Paragraph(award_text, normal_style))
            story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Skills
    skills = resume_data.get('skills', [])
    if skills:
        story.append(Paragraph("<b>Skills</b>", heading_style))
        for skill in skills:
            name = skill.get('name', '')
            keywords = skill.get('keywords', [])
            
            skill_text = f"<b>{name}</b>"
            if keywords:
                skill_text += f": {', '.join(keywords)}"
            
            story.append(Paragraph(skill_text, normal_style))
            story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.1*inch))
    
    # Languages
    languages = resume_data.get('languages', [])
    if languages:
        story.append(Paragraph("<b>Languages</b>", heading_style))
        lang_list = []
        for lang in languages:
            language = lang.get('language', '')
            fluency = lang.get('fluency', '')
            if language and fluency:
                lang_list.append(f"{language} ({fluency})")
        if lang_list:
            story.append(Paragraph(", ".join(lang_list), normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Certificates
    certificates = resume_data.get('certificates', [])
    if certificates:
        filtered_certs = [c for c in certificates if c.get('name') and c.get('name').strip()]
        if filtered_certs:
            story.append(Paragraph("<b>Certificates</b>", heading_style))
            for cert in filtered_certs:
                name = cert.get('name', '')
                issuer = cert.get('issuer', '')
                date = format_date(cert.get('date', ''))
                
                cert_text = f"<b>{name}</b>"
                if issuer:
                    cert_text += f" | {issuer}"
                if date:
                    cert_text += f" ({date})"
                
                story.append(Paragraph(cert_text, normal_style))
                story.append(Spacer(1, 0.05*inch))
            story.append(Spacer(1, 0.1*inch))
    
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
    create_cv_pdf(resume_data, output_path)

if __name__ == '__main__':
    main()

