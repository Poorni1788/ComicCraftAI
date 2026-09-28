import os
from datetime import datetime
from fpdf import FPDF

class PDF(FPDF):
    pass

FONT_PATH = "static/fonts/DejaVuSans.ttf"
EXPORT_FOLDER = "static/exports"

def save_pdf(layout):
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add Unicode font (if font file exists)
    if os.path.exists(FONT_PATH):
        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
        pdf.set_font('DejaVu', '', 12)
    else:
        pdf.set_font('Helvetica', '', 12)

    for panel in layout:
        image_path = panel.get('image_path', '')
        story_text = panel.get('text', '')

        pdf.add_page()

        # Panel title
        if os.path.exists(FONT_PATH):
            pdf.set_font('DejaVu', '', 14)
        else:
            pdf.set_font('Helvetica', 'B', 14)
            
        pdf.cell(0, 10, f"Panel {panel.get('panel', '')}", ln=True, align="C")
        
        if os.path.exists(FONT_PATH):
            pdf.set_font('DejaVu', '', 12)
        else:
            pdf.set_font('Helvetica', '', 12)

        # Image placement
        y_image = 30
        image_height = 100

        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=y_image, w=pdf.w - 20, h=image_height)
        else:
            pdf.set_y(y_image)
            pdf.multi_cell(0, 10, f"Image missing: {image_path}")

        # Text placement below image
        pdf.set_y(y_image + image_height + 15)
        story_lines = story_text.strip().splitlines()
        if story_lines and story_lines[0].strip().lower().startswith("**panel"):
            story_lines = story_lines[1:]
        cleaned_text = "\n".join(story_lines).strip()
        pdf.multi_cell(0, 10, cleaned_text)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)

    return pdf_path
