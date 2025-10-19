from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from docx import Document
from analyzer import simple_skill_extractor, detect_sections, calculate_completeness

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

@app.post("/generate_resume")
async def generate_resume(file: UploadFile = File(...)):
    # 1️⃣ Extract text
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file.file)
    else:
        return {"error": "Unsupported file type"}

    # 2️⃣ Analyze
    result = simple_skill_extractor(text)
    skills = result["skills_found"]
    found_sections, missing_sections = detect_sections(text)
    suggestions = [f"Add {sec} section" for sec in missing_sections]

    # 3️⃣ Generate PDF
    output_file = "improved_resume.pdf"
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Improved Resume")
    y -= 30

    # Original snippet
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Original Text Snippet:")
    y -= 20
    for line in text[:1000].split("\n"):
        c.drawString(50, y, line[:80])
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    y -= 20
    # Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detected Skills:")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, ", ".join(skills))
    y -= 30

    # Suggestions
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Improvement Suggestions:")
    y -= 20
    c.setFont("Helvetica", 12)
    for s in suggestions:
        c.drawString(50, y, f"- {s}")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

    return FileResponse(output_file, media_type="application/pdf", filename="improved_resume.pdf")

# Helper: extract PDF text
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n".join(pages)

# Helper: extract DOCX text
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    # 1️⃣ Extract text based on file type
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file.file)
    else:
        return {"error": "Unsupported file type. Use PDF or DOCX."}

    # 2️⃣ Detect skills
    result = simple_skill_extractor(text)
    skills = result["skills_found"]

    # 3️⃣ Detect sections
    found_sections, missing_sections = detect_sections(text)

    # 4️⃣ Calculate completeness
    completeness = calculate_completeness(found_sections, skills)

    # 5️⃣ Suggestions
    suggestions = [f"Add {sec} section" for sec in missing_sections]

    return {
        "text_snippet": text[:1000],
        "skills_detected": skills,
        "top_words": result["top_words"],
        "found_sections": found_sections,
        "completeness": completeness,
        "suggestions": suggestions
    }
