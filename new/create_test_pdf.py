from reportlab.pdfgen import canvas

def create_test_pdf():
    c = canvas.Canvas("example.pdf")
    c.drawString(100, 750, "OSINT Test PDF")
    c.drawString(100, 730, "This is a test PDF for OSINT examples.")
    c.save()

create_test_pdf()