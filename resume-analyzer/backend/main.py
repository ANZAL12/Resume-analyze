from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import pdfplumber
from docx import Document
from analyzer import (
    advanced_skill_extractor, detect_sections_advanced, calculate_completeness_advanced,
    analyze_keyword_density, calculate_ats_score, analyze_content_quality,
    generate_improvement_suggestions, ATS_KEYWORDS, simple_skill_extractor, detect_sections
)
import json
import os
from datetime import datetime

app = FastAPI()

# CORS middleware - Allow all origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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
    """Advanced resume analysis with comprehensive insights"""
    try:
        # 1️⃣ Extract text based on file type
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file.file)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or DOCX.")

        # 2️⃣ Advanced skill analysis
        skills_advanced = advanced_skill_extractor(text)
        skills_simple = [skill["skill"] for skill in skills_advanced]

        # 3️⃣ Section analysis
        found_sections, missing_sections = detect_sections_advanced(text)

        # 4️⃣ ATS optimization analysis
        ats_score, ats_checks = calculate_ats_score(text)
        keyword_analysis = analyze_keyword_density(text, ATS_KEYWORDS)

        # 5️⃣ Content quality analysis
        content_analysis = analyze_content_quality(text)

        # 6️⃣ Calculate advanced completeness
        completeness = calculate_completeness_advanced(found_sections, skills_advanced, ats_score)

        # 7️⃣ Generate comprehensive suggestions
        suggestions = generate_improvement_suggestions(text, skills_advanced, found_sections, ats_score)

        # 8️⃣ Skill categorization
        skills_by_category = {}
        for skill in skills_advanced:
            category = skill["category"]
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)

        return {
            "text_snippet": text[:1000],
            "skills_detected": skills_simple,
            "skills_advanced": skills_advanced,
            "skills_by_category": skills_by_category,
            "found_sections": found_sections,
            "missing_sections": missing_sections,
            "completeness": completeness,
            "ats_score": ats_score,
            "ats_checks": ats_checks,
            "keyword_analysis": keyword_analysis,
            "content_analysis": content_analysis,
            "suggestions": suggestions,
            "analysis_timestamp": datetime.now().isoformat(),
            "file_info": {
                "filename": file.filename,
                "file_size": len(text),
                "word_count": content_analysis["word_count"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/analysis/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.options("/analyze")
async def analyze_options():
    """Handle preflight requests for CORS"""
    return {"message": "OK"}

@app.get("/")
async def root():
    """Root endpoint with CORS headers"""
    return {"message": "Resume Analyzer API is running", "cors": "enabled"}

@app.post("/analysis/compare")
async def compare_resumes(files: list[UploadFile] = File(...)):
    """Compare multiple resumes"""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least 2 files required for comparison")
    
    results = []
    for file in files:
        try:
            if file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(file.file)
            elif file.filename.endswith(".docx"):
                text = extract_text_from_docx(file.file)
            else:
                continue
            
            skills = advanced_skill_extractor(text)
            sections, _ = detect_sections_advanced(text)
            ats_score, _ = calculate_ats_score(text)
            
            results.append({
                "filename": file.filename,
                "skills_count": len(skills),
                "sections_count": len(sections),
                "ats_score": ats_score,
                "skills": [skill["skill"] for skill in skills]
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {"comparison_results": results}

@app.post("/analysis/export")
async def export_analysis(file: UploadFile = File(...), format: str = "json"):
    """Export detailed analysis in various formats"""
    try:
        # Perform analysis
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file.file)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Get comprehensive analysis
        skills_advanced = advanced_skill_extractor(text)
        found_sections, missing_sections = detect_sections_advanced(text)
        ats_score, ats_checks = calculate_ats_score(text)
        content_analysis = analyze_content_quality(text)
        
        analysis_data = {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "skills": skills_advanced,
            "sections": {
                "found": found_sections,
                "missing": missing_sections
            },
            "ats_score": ats_score,
            "ats_checks": ats_checks,
            "content_analysis": content_analysis,
            "text_preview": text[:500]
        }
        
        if format.lower() == "json":
            return JSONResponse(content=analysis_data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported export format")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
