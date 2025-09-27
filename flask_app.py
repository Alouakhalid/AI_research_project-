from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import tempfile
from datetime import datetime
import os

# Import our AI model
from AImodel import ai_generator

app = Flask(__name__)

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
    """Download research paper as PDF"""
    try:
        data = request.get_json()
        research_paper = data.get('research_paper', '')
        topic = data.get('topic', 'Research Paper')
        language = data.get('language', 'English')
        
        if not research_paper:
            return jsonify({'error': 'No research paper content to convert'}), 400
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=0
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph(f"<b>{topic}</b>", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Language: {language}", normal_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Split content into paragraphs and format
        paragraphs = research_paper.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Check if it's a heading (starts with common heading words)
            if any(para.lower().startswith(word) for word in ['abstract', 'introduction', 'literature review', 'methodology', 'results', 'discussion', 'conclusion', 'references']):
                story.append(Paragraph(f"<b>{para}</b>", heading_style))
            else:
                # Regular paragraph
                story.append(Paragraph(para, normal_style))
            
            story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(buffer.getvalue())
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"{topic.replace(' ', '_')}_Research_Paper.pdf",
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
    print("🚀 Starting AI Research Paper Generator...")
    print("🤖 Using Gemini 2.5 Flash model")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Check if AI model is ready
    if ai_generator.is_ready():
        print("✅ AI model is ready!")
    else:
        print("❌ AI model not ready. Please check your API key in .env file")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
