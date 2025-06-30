from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pathlib import Path

def create_mock_non_invoice():
    """Create a mock document that should be flagged as invalid (not an invoice)."""
    
    # Create the output directory if it doesn't exist
    output_dir = Path("classwork/invoice_reader/invoices")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        str(output_dir / "mock_non_invoice.pdf"),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Story to hold all elements
    story = []
    
    # Add title
    story.append(Paragraph("LETTER OF RECOMMENDATION", title_style))
    story.append(Spacer(1, 12))
    
    # Add date
    story.append(Paragraph("January 15, 2024", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Add recipient
    story.append(Paragraph("To Whom It May Concern,", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Add letter content
    story.append(Paragraph("I am writing this letter to recommend John Smith for the position of Software Engineer at your company. "
                          "I have had the pleasure of working with John for the past three years at TechCorp, where he has consistently "
                          "demonstrated exceptional technical skills and professional integrity.", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("During his time at TechCorp, John has been responsible for developing and maintaining several critical "
                          "applications. His expertise in Python, JavaScript, and database management has been invaluable to our team. "
                          "He has consistently delivered high-quality code and has been a mentor to junior developers.", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("John's problem-solving abilities are outstanding. He has a unique talent for breaking down complex "
                          "technical challenges into manageable components and finding elegant solutions. His attention to detail "
                          "and commitment to writing clean, maintainable code sets him apart from many other developers.", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Beyond his technical skills, John is an excellent team player. He communicates effectively with both "
                          "technical and non-technical stakeholders, and he is always willing to help his colleagues. His positive "
                          "attitude and strong work ethic make him a valuable asset to any organization.", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("I am confident that John would be an excellent addition to your team. He has my highest recommendation "
                          "and I believe he would make significant contributions to your organization.", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("If you have any questions about John's qualifications or experience, please do not hesitate to contact me.", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Add signature
    story.append(Paragraph("Sincerely,", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Jane Doe", styles['Normal']))
    story.append(Paragraph("Senior Software Engineer", styles['Normal']))
    story.append(Paragraph("TechCorp Inc.", styles['Normal']))
    story.append(Paragraph("Email: jane.doe@techcorp.com", styles['Normal']))
    story.append(Paragraph("Phone: (555) 987-6543", styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    print("Created mock non-invoice document: mock_non_invoice.pdf")

if __name__ == "__main__":
    create_mock_non_invoice() 