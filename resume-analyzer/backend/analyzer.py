# backend/analyzer.py
import re
from collections import Counter

# Skills to detect
CANDIDATE_LABELS = [
    "python","java","c++","javascript","react","django",
    "machine learning","deep learning","data analysis",
    "project management","leadership","communication",
    "aws","docker","kubernetes","sql","git","problem solving"
]

SECTIONS = ["education", "experience", "projects", "skills", "summary", "contact"]

def simple_skill_extractor(text):
    text_lower = text.lower()
    found = [s for s in CANDIDATE_LABELS if s in text_lower]
    freq = Counter(re.findall(r'\w+', text_lower))
    return {"skills_found": found, "top_words": freq.most_common(20)}

def detect_sections(text):
    text_lower = text.lower()
    found = [s for s in SECTIONS if s in text_lower]
    missing = [s for s in SECTIONS if s not in text_lower]
    return found, missing

def calculate_completeness(found_sections, skills_detected):
    section_score = len(found_sections) / len(SECTIONS)
    skill_score = min(len(skills_detected) / 10, 1.0)  # Cap skill score at 10 skills
    return round((section_score + skill_score) / 2 * 100)
