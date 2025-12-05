from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE (Dark Mode Theme) ---
DARK_BG = RGBColor(14, 17, 23)       # #0E1117 (Your Dashboard Background)
NEON_PURPLE = RGBColor(124, 58, 237) # #7C3AED (Aries Brand Color)
NEON_GREEN = RGBColor(0, 255, 127)   # Success Green
NEON_PINK = RGBColor(219, 39, 119)   # Alert Pink
TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_GREY = RGBColor(178, 181, 190)

def set_dark_background(slide):
    """Sets the slide background to the Aries Dark Grey."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG

def add_neon_title(slide, text):
    """Adds a large, glowing title."""
    title_shape = slide.shapes.title
    title_shape.text = text
    
    # Styling
    p = title_shape.text_frame.paragraphs[0]
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.name = "Arial Black"
    p.font.color.rgb = NEON_PURPLE
    p.alignment = PP_ALIGN.LEFT
    
    # Move title up slightly
    title_shape.top = Inches(0.5)
    title_shape.left = Inches(0.5)

def add_bullet_points(slide, points, accent_color=TEXT_WHITE):
    """Adds catchy bullet points with custom colors."""
    left = Inches(0.5)
    top = Inches(1.8)
    width = Inches(9)
    height = Inches(5)
    
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    
    for point in points:
        p = tf.add_paragraph()
        p.text = "▶  " + point  # Custom arrow bullet
        p.font.size = Pt(28)
        p.font.color.rgb = accent_color
        p.space_after = Pt(20) # Space between points

# --- MAIN SCRIPT ---
prs = Presentation()

# SLIDE 1: TITLE SLIDE (The Hook)
slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
set_dark_background(slide)

# Big Title
txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2))
p = txBox.text_frame.paragraphs[0]
p.text = "ARIES"
p.font.size = Pt(96)
p.font.bold = True
p.font.color.rgb = NEON_PURPLE
p.alignment = PP_ALIGN.CENTER

# Subtitle
txBox2 = slide.shapes.add_textbox(Inches(1), Inches(4), Inches(8), Inches(1))
p2 = txBox2.text_frame.add_paragraph()
p2.text = "REAL-TIME BRAND INTELLIGENCE"
p2.font.size = Pt(32)
p2.font.color.rgb = NEON_GREEN
p2.alignment = PP_ALIGN.CENTER

# Team Name
txBox3 = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(8), Inches(1))
p3 = txBox3.text_frame.add_paragraph()
p3.text = "Team Science | Advait Jishnani"
p3.font.size = Pt(18)
p3.font.color.rgb = TEXT_GREY
p3.alignment = PP_ALIGN.CENTER


# SLIDE 2: THE PROBLEM (High Contrast)
slide = prs.slides.add_slide(prs.slide_layouts[5])
set_dark_background(slide)
add_neon_title(slide, "THE PROBLEM")
add_bullet_points(slide, [
    "Brand reputation is destroyed in minutes.",
    "Companies are currently 'Flying Blind'.",
    "Weekly reports are too slow.",
    "We need a LIVE PULSE of sentiment."
], TEXT_WHITE)


# SLIDE 3: THE SOLUTION (Architecture)
slide = prs.slides.add_slide(prs.slide_layouts[5])
set_dark_background(slide)
add_neon_title(slide, "THE ARCHITECTURE")

# Draw a visual flow using shapes instead of boring text
shapes = slide.shapes
# Box 1: Ingestion
box1 = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(3), Inches(2.5), Inches(1.5))
box1.fill.solid()
box1.fill.fore_color.rgb = NEON_PURPLE
box1.text_frame.text = "INGESTION\n(Social Firehose)"

# Arrow 1
arrow1 = shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.1), Inches(3.5), Inches(1), Inches(0.5))
arrow1.fill.solid()
arrow1.fill.fore_color.rgb = TEXT_GREY

# Box 2: Processing
box2 = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.2), Inches(3), Inches(2.5), Inches(1.5))
box2.fill.solid()
box2.fill.fore_color.rgb = NEON_PINK
box2.text_frame.text = "PROCESSING\n(VADER + EMA)"

# Arrow 2
arrow2 = shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.8), Inches(3.5), Inches(1), Inches(0.5))
arrow2.fill.solid()
arrow2.fill.fore_color.rgb = TEXT_GREY

# Box 3: Dashboard (THE FIX WAS HERE: Inches(2.5) instead of 2, 5)
box3 = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(3), Inches(2.5), Inches(1.5))
box3.fill.solid()
box3.fill.fore_color.rgb = NEON_GREEN
box3.text_frame.text = "DASHBOARD\n(Streamlit)"


# SLIDE 4: LIVE DEMO (Big Impact)
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_dark_background(slide)
txBox = slide.shapes.add_textbox(Inches(0), Inches(2.5), Inches(10), Inches(2))
p = txBox.text_frame.paragraphs[0]
p.text = "LIVE DEMO"
p.font.size = Pt(80)
p.font.bold = True
p.font.color.rgb = NEON_GREEN
p.alignment = PP_ALIGN.CENTER


# SLIDE 5: IMPACT & FUTURE
slide = prs.slides.add_slide(prs.slide_layouts[5])
set_dark_background(slide)
add_neon_title(slide, "WHY IT MATTERS")
add_bullet_points(slide, [
    "Response time reduced: 24h ➔ 10 seconds.",
    "Exponential Moving Average filters noise.",
    "Scalable: Ready for Kafka & Spark.",
    "Status: PRODUCTION READY."
], TEXT_WHITE)

# Save
prs.save('Aries_Catchy.pptx')
print("✅ Created 'Aries_Catchy.pptx' with Dark Mode & Neon Colors!")