import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _sanitize_filename(self, topic):
        """Convert topic to valid filename."""
        # Remove special characters, replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', topic)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.lower()
    
    def generate_filename(self, topic):
        """Generate timestamped filename for PDF."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = self._sanitize_filename(topic)
        return f"{sanitized_topic}_{timestamp}.pdf"
    
    def _format_content_for_pdf(self, content):
        """Format the article content for better PDF readability."""
        # Clean up the content
        formatted_content = content.strip()
        
        # Replace multiple newlines with proper paragraph breaks
        formatted_content = re.sub(r'\n\s*\n', '<br/><br/>', formatted_content)
        
        # Replace single newlines with spaces (for better paragraph flow)
        formatted_content = re.sub(r'(?<!\n)\n(?!\n)', ' ', formatted_content)
        
        # Handle bullet points and numbered lists
        formatted_content = re.sub(r'^\s*[-•*]\s+', '• ', formatted_content, flags=re.MULTILINE)
        formatted_content = re.sub(r'^\s*(\d+)\.\s+', r'\1. ', formatted_content, flags=re.MULTILINE)
        
        # Clean up extra spaces
        formatted_content = re.sub(r'\s+', ' ', formatted_content)
        
        return formatted_content
    
    def create_pdf(self, topic, article_content):
        """Create a formatted PDF with the article content."""
        filename = self.generate_filename(topic)
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1,  # Center alignment
                textColor='#2E4053'
            )
            story.append(Paragraph(topic, title_style))
            story.append(Spacer(1, 12))
            
            # Generation timestamp
            timestamp_style = ParagraphStyle(
                'Timestamp',
                parent=styles['Normal'],
                fontSize=10,
                textColor='#7F8C8D',
                alignment=1
            )
            timestamp = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
            story.append(Paragraph(timestamp, timestamp_style))
            story.append(Spacer(1, 20))
            
            # Format the article content
            formatted_content = self._format_content_for_pdf(article_content)
            
            # Article content with better styling
            content_style = ParagraphStyle(
                'Content',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                alignment=0,  # Left alignment
                leading=18,  # Line spacing
                textColor='#2C3E50'
            )
            
            # Split content into paragraphs for better formatting
            paragraphs = formatted_content.split('<br/><br/>')
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Handle bullet points
                    if paragraph.strip().startswith('•'):
                        bullet_style = ParagraphStyle(
                            'Bullet',
                            parent=content_style,
                            leftIndent=20,
                            firstLineIndent=-10
                        )
                        story.append(Paragraph(paragraph.strip(), bullet_style))
                    else:
                        story.append(Paragraph(paragraph.strip(), content_style))
                    story.append(Spacer(1, 8))
            
            # Build PDF
            doc.build(story)
            return filepath
            
        except Exception as e:
            raise Exception(f"PDF generation failed: {str(e)}") 