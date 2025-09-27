from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
import tempfile
from datetime import datetime
import os
import arabic_reshaper
from bidi.algorithm import get_display

# Import our AI model
from AImodel import ai_generator

app = Flask(__name__)

# Setup Arabic fonts
def setup_arabic_fonts():
    """Setup Arabic fonts for PDF generation"""
    try:
        # Try to register common Arabic fonts
        font_paths = [
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/System/Library/Fonts/Arial.ttf',  # macOS
            'C:/Windows/Fonts/arial.ttf',  # Windows
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ArabicFont', font_path))
                    return True
                except:
                    continue
        
        # Fallback to default font
        return False
    except:
        return False

def process_arabic_text(text, language):
    """Process Arabic text for proper display"""
    if language.lower() in ['arabic', 'العربية']:
        try:
            # Reshape Arabic text
            reshaped_text = arabic_reshaper.reshape(text)
            # Apply bidirectional algorithm
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except:
            return text
    return text

def create_professional_styles():
    """Create professional styles for the research paper"""
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica'
    )
    
    # Heading styles
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # Abstract style
    abstract_style = ParagraphStyle(
        'CustomAbstract',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leftIndent=20,
        rightIndent=20
    )
    
    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'heading1': heading1_style,
        'heading2': heading2_style,
        'normal': normal_style,
        'abstract': abstract_style
    }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_research():
    """Generate research paper using AI"""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        language = data.get('language', 'English')
        pages = data.get('pages', '3')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Check if AI model is ready
        if not ai_generator.is_ready():
            return jsonify({'error': 'AI model not available. Please check your API key.'}), 500
        
        # Generate research paper using our AI model
        result = ai_generator.generate_research_paper(topic, language, pages)
        
        if result['success']:
            return jsonify({
                'success': True,
                'research_paper': result['research_paper'],
                'topic': result['topic'],
                'language': result['language'],
                'pages': result['pages'],
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error generating research paper: {str(e)}'}), 500

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    """Download research paper as professional PDF"""
    try:
        data = request.get_json()
        research_paper = data.get('research_paper', '')
        topic = data.get('topic', 'Research Paper')
        language = data.get('language', 'English')
        
        if not research_paper:
            return jsonify({'error': 'No research paper content to convert'}), 400
        
        # Setup Arabic fonts if needed
        setup_arabic_fonts()
        
        # Create PDF with professional margins
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            rightMargin=72, 
            leftMargin=72, 
            topMargin=72, 
            bottomMargin=72
        )
        
        # Get professional styles
        styles = create_professional_styles()
        
        # Build PDF content
        story = []
        
        # COVER PAGE
        story.append(Spacer(1, 2*inch))
        
        # University/Institution (placeholder)
        institution_text = process_arabic_text("جامعة البحث العلمي" if language.lower() in ['arabic', 'العربية'] else "Research University", language)
        story.append(Paragraph(f"<b>{institution_text}</b>", styles['subtitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Main Title
        title_text = process_arabic_text(topic, language)
        story.append(Paragraph(f"<b>{title_text}</b>", styles['title']))
        story.append(Spacer(1, 0.8*inch))
        
        # Subtitle
        subtitle_text = process_arabic_text("ورقة بحثية" if language.lower() in ['arabic', 'العربية'] else "Research Paper", language)
        story.append(Paragraph(f"<i>{subtitle_text}</i>", styles['subtitle']))
        story.append(Spacer(1, 1*inch))
        
        # Author information
        author_text = process_arabic_text("مقدم من: الباحث" if language.lower() in ['arabic', 'العربية'] else "Prepared by: Researcher", language)
        story.append(Paragraph(author_text, styles['normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Date
        date_text = process_arabic_text(f"تاريخ الإعداد: {datetime.now().strftime('%B %d, %Y')}" if language.lower() in ['arabic', 'العربية'] else f"Date: {datetime.now().strftime('%B %d, %Y')}", language)
        story.append(Paragraph(date_text, styles['normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Language
        lang_text = process_arabic_text(f"اللغة: {language}" if language.lower() in ['arabic', 'العربية'] else f"Language: {language}", language)
        story.append(Paragraph(lang_text, styles['normal']))
        
        # Page break after cover
        story.append(PageBreak())
        
        # TABLE OF CONTENTS
        toc_title = process_arabic_text("جدول المحتويات" if language.lower() in ['arabic', 'العربية'] else "Table of Contents", language)
        story.append(Paragraph(f"<b>{toc_title}</b>", styles['heading1']))
        story.append(Spacer(1, 0.3*inch))
        
        # TOC entries
        toc_entries = [
            ("1. " + ("الملخص" if language.lower() in ['arabic', 'العربية'] else "Abstract"), "1"),
            ("2. " + ("المقدمة" if language.lower() in ['arabic', 'العربية'] else "Introduction"), "2"),
            ("3. " + ("مراجعة الأدبيات" if language.lower() in ['arabic', 'العربية'] else "Literature Review"), "3"),
            ("4. " + ("المنهجية" if language.lower() in ['arabic', 'العربية'] else "Methodology"), "4"),
            ("5. " + ("النتائج" if language.lower() in ['arabic', 'العربية'] else "Results"), "5"),
            ("6. " + ("المناقشة" if language.lower() in ['arabic', 'العربية'] else "Discussion"), "6"),
            ("7. " + ("الخلاصة" if language.lower() in ['arabic', 'العربية'] else "Conclusion"), "7"),
            ("8. " + ("المراجع" if language.lower() in ['arabic', 'العربية'] else "References"), "8"),
            ("9. " + ("الملاحق" if language.lower() in ['arabic', 'العربية'] else "Appendix"), "9")
        ]
        
        for entry, page in toc_entries:
            entry_text = process_arabic_text(entry, language)
            story.append(Paragraph(f"{entry_text} ................ {page}", styles['normal']))
        
        story.append(PageBreak())
        
        # MAIN CONTENT
        # Process and format the research paper content
        paragraphs = research_paper.split('\n\n')
        section_number = 1
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Process Arabic text
            processed_para = process_arabic_text(para, language)
            
            # Check if it's a major heading
            if any(processed_para.lower().startswith(word) for word in ['abstract', 'introduction', 'literature review', 'methodology', 'results', 'discussion', 'conclusion', 'references', 'الملخص', 'المقدمة', 'مراجعة الأدبيات', 'المنهجية', 'النتائج', 'المناقشة', 'الخلاصة', 'المراجع']):
                section_number += 1
                story.append(Paragraph(f"<b>{processed_para}</b>", styles['heading1']))
            elif any(processed_para.lower().startswith(word) for word in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']):
                story.append(Paragraph(f"<b>{processed_para}</b>", styles['heading2']))
            else:
                # Regular paragraph
                if 'abstract' in processed_para.lower() or 'ملخص' in processed_para:
                    story.append(Paragraph(processed_para, styles['abstract']))
                else:
                    story.append(Paragraph(processed_para, styles['normal']))
            
            story.append(Spacer(1, 6))
        
        # APPENDIX SECTION
        story.append(PageBreak())
        appendix_title = process_arabic_text("الملاحق" if language.lower() in ['arabic', 'العربية'] else "Appendix", language)
        story.append(Paragraph(f"<b>{appendix_title}</b>", styles['heading1']))
        story.append(Spacer(1, 0.3*inch))
        
        # Appendix content
        appendix_content = process_arabic_text(
            "هذا القسم يحتوي على معلومات إضافية ومراجع إضافية للورقة البحثية." if language.lower() in ['arabic', 'العربية'] 
            else "This section contains additional information and supplementary references for the research paper.",
            language
        )
        story.append(Paragraph(appendix_content, styles['normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Additional appendix items
        appendix_items = [
            "A. " + ("الرسوم البيانية" if language.lower() in ['arabic', 'العربية'] else "Charts and Graphs"),
            "B. " + ("البيانات الإحصائية" if language.lower() in ['arabic', 'العربية'] else "Statistical Data"),
            "C. " + ("المراجع الإضافية" if language.lower() in ['arabic', 'العربية'] else "Additional References"),
            "D. " + ("الملاحظات" if language.lower() in ['arabic', 'العربية'] else "Notes and Comments")
        ]
        
        for item in appendix_items:
            item_text = process_arabic_text(item, language)
            story.append(Paragraph(f"<b>{item_text}</b>", styles['heading2']))
            story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(buffer.getvalue())
        temp_file.close()
        
        # Clean filename
        clean_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{clean_topic}_Research_Paper.pdf"
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error creating PDF: {str(e)}'}), 500

@app.route('/status')
def status():
    """Check AI model status"""
    return jsonify({
        'ai_ready': ai_generator.is_ready(),
        'model': 'gemini-2.5-flash'
    })

if __name__ == '__main__':
    import os
    
    print("🚀 Starting AI Research Paper Generator...")
    print("🤖 Using Gemini 2.5 Flash model")
    
    # Check if AI model is ready
    if ai_generator.is_ready():
        print("✅ AI model is ready!")
    else:
        print("❌ AI model not ready. Please check your API key in .env file")
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    if debug:
        print("📍 Open your browser and go to: http://localhost:8080")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
