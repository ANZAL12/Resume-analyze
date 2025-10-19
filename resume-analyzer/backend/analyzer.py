# Advanced Resume Analyzer
import re
import math
from collections import Counter, defaultdict
from datetime import datetime

# Enhanced skills database with categories and synonyms
SKILLS_DATABASE = {
    "Programming Languages": {
        "python": ["python", "py", "django", "flask", "fastapi", "pandas", "numpy"],
        "java": ["java", "spring", "hibernate", "maven", "gradle"],
        "javascript": ["javascript", "js", "node", "nodejs", "express"],
        "c++": ["c++", "cpp", "cplusplus"],
        "c#": ["c#", "csharp", ".net", "dotnet"],
        "go": ["go", "golang"],
        "rust": ["rust", "rustlang"],
        "php": ["php", "laravel", "symfony"],
        "ruby": ["ruby", "rails", "ror"]
    },
    "Frameworks & Libraries": {
        "react": ["react", "reactjs", "jsx", "redux", "nextjs"],
        "angular": ["angular", "angularjs", "ng"],
        "vue": ["vue", "vuejs", "nuxt"],
        "django": ["django", "djangorest"],
        "flask": ["flask", "fastapi"],
        "spring": ["spring", "springboot", "springboot"],
        "express": ["express", "expressjs"]
    },
    "Cloud & DevOps": {
        "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
        "azure": ["azure", "microsoft azure"],
        "gcp": ["gcp", "google cloud", "gce"],
        "docker": ["docker", "containerization"],
        "kubernetes": ["kubernetes", "k8s", "kubectl"],
        "terraform": ["terraform", "iac"],
        "jenkins": ["jenkins", "ci/cd"]
    },
    "Data & AI": {
        "machine learning": ["machine learning", "ml", "ai", "artificial intelligence"],
        "data science": ["data science", "data analysis", "analytics"],
        "sql": ["sql", "mysql", "postgresql", "mongodb", "database"],
        "tensorflow": ["tensorflow", "tf"],
        "pytorch": ["pytorch", "torch"],
        "pandas": ["pandas", "dataframe"],
        "numpy": ["numpy", "numerical computing"]
    },
    "Soft Skills": {
        "leadership": ["leadership", "team lead", "management"],
        "communication": ["communication", "presentation", "writing"],
        "project management": ["project management", "agile", "scrum", "kanban"],
        "problem solving": ["problem solving", "analytical", "critical thinking"]
    }
}

# Industry keywords for ATS optimization
ATS_KEYWORDS = {
    "software engineer": ["software", "development", "programming", "coding", "engineering"],
    "data scientist": ["data", "analysis", "machine learning", "statistics", "python", "r"],
    "product manager": ["product", "management", "strategy", "roadmap", "stakeholder"],
    "marketing": ["marketing", "campaign", "digital", "social media", "seo", "analytics"],
    "sales": ["sales", "revenue", "client", "customer", "business development"],
    "finance": ["finance", "financial", "accounting", "budget", "analysis", "excel"]
}

# Resume sections with synonyms
SECTIONS = {
    "contact": ["contact", "personal", "info", "details"],
    "summary": ["summary", "profile", "objective", "about"],
    "experience": ["experience", "work", "employment", "career", "professional"],
    "education": ["education", "academic", "degree", "university", "college"],
    "skills": ["skills", "technical", "technologies", "tools", "competencies"],
    "projects": ["projects", "portfolio", "work samples", "achievements"],
    "certifications": ["certifications", "certificates", "credentials", "licenses"]
}

def advanced_skill_extractor(text):
    """Enhanced skill extraction with confidence scoring and categorization"""
    text_lower = text.lower()
    detected_skills = []
    
    for category, skills in SKILLS_DATABASE.items():
        for skill_name, variations in skills.items():
            confidence = 0
            matches = []
            
            for variation in variations:
                # Exact word matches (higher confidence)
                if re.search(r'\b' + re.escape(variation) + r'\b', text_lower):
                    confidence += 0.8
                    matches.append(variation)
                # Partial matches (lower confidence)
                elif variation in text_lower:
                    confidence += 0.4
                    matches.append(variation)
            
            if confidence > 0.3:  # threshold for detection
                detected_skills.append({
                    "skill": skill_name,
                    "category": category,
                    "confidence": round(confidence, 2),
                    "matches": matches,
                    "variations_found": len(matches)
                })
    
    # Sort by confidence
    detected_skills.sort(key=lambda x: x["confidence"], reverse=True)
    return detected_skills

def detect_sections_advanced(text):
    """Advanced section detection with synonyms"""
    text_lower = text.lower()
    found_sections = []
    missing_sections = []
    
    for section_name, synonyms in SECTIONS.items():
        found = False
        for synonym in synonyms:
            if synonym in text_lower:
                found = True
                break
        
        if found:
            found_sections.append(section_name)
        else:
            missing_sections.append(section_name)
    
    return found_sections, missing_sections

def analyze_keyword_density(text, target_keywords):
    """Analyze keyword density for ATS optimization"""
    text_lower = text.lower()
    word_count = len(text_lower.split())
    keyword_analysis = {}
    
    for keyword, variations in target_keywords.items():
        total_occurrences = 0
        for variation in variations:
            total_occurrences += len(re.findall(r'\b' + re.escape(variation) + r'\b', text_lower))
        
        density = (total_occurrences / word_count * 100) if word_count > 0 else 0
        keyword_analysis[keyword] = {
            "count": total_occurrences,
            "density": round(density, 2),
            "score": min(density * 10, 100)  # Score out of 100
        }
    
    return keyword_analysis

def calculate_ats_score(text):
    """Calculate ATS (Applicant Tracking System) optimization score"""
    text_lower = text.lower()
    
    # Check for common ATS-friendly elements
    ats_checks = {
        "has_contact_info": bool(re.search(r'(email|phone|address|linkedin)', text_lower)),
        "has_summary": bool(re.search(r'(summary|profile|objective)', text_lower)),
        "has_skills_section": bool(re.search(r'(skills|technical|technologies)', text_lower)),
        "has_experience": bool(re.search(r'(experience|work|employment)', text_lower)),
        "has_education": bool(re.search(r'(education|degree|university)', text_lower)),
        "has_quantifiable_results": bool(re.search(r'(\d+%|\$\d+|\d+\+|\d+x)', text_lower)),
        "has_action_verbs": bool(re.search(r'(developed|created|managed|led|implemented|achieved)', text_lower)),
        "proper_formatting": bool(re.search(r'(•|\*|\d+\.)', text_lower))  # Bullet points or numbered lists
    }
    
    score = sum(ats_checks.values()) / len(ats_checks) * 100
    return round(score), ats_checks

def analyze_content_quality(text):
    """Analyze content quality and provide insights"""
    text_lower = text.lower()
    word_count = len(text_lower.split())
    
    # Check for common issues
    issues = []
    suggestions = []
    
    # Length analysis
    if word_count < 200:
        issues.append("Resume is too short")
        suggestions.append("Add more details about your experience and achievements")
    elif word_count > 800:
        issues.append("Resume might be too long")
        suggestions.append("Consider condensing content to 1-2 pages")
    
    # Check for action verbs
    action_verbs = ["achieved", "developed", "created", "managed", "led", "implemented", 
                   "designed", "built", "improved", "increased", "reduced", "optimized"]
    action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    
    if action_verb_count < 3:
        issues.append("Limited use of action verbs")
        suggestions.append("Use more strong action verbs to describe your achievements")
    
    # Check for quantifiable results
    numbers = re.findall(r'\d+', text_lower)
    if len(numbers) < 2:
        issues.append("Limited quantifiable achievements")
        suggestions.append("Add specific numbers, percentages, or metrics to your achievements")
    
    # Check for keywords
    keyword_density = analyze_keyword_density(text, ATS_KEYWORDS)
    avg_density = sum(k["density"] for k in keyword_density.values()) / len(keyword_density)
    
    if avg_density < 1.0:
        issues.append("Low keyword density")
        suggestions.append("Include more industry-relevant keywords")
    
    return {
        "word_count": word_count,
        "issues": issues,
        "suggestions": suggestions,
        "action_verb_count": action_verb_count,
        "number_count": len(numbers),
        "keyword_density": avg_density
    }

def generate_improvement_suggestions(text, skills_detected, sections_found, ats_score):
    """Generate comprehensive improvement suggestions"""
    suggestions = []
    
    # Section-based suggestions
    if "summary" not in sections_found:
        suggestions.append("Add a professional summary section highlighting your key strengths")
    
    if "skills" not in sections_found:
        suggestions.append("Create a dedicated skills section to showcase your technical abilities")
    
    if "projects" not in sections_found:
        suggestions.append("Include a projects section to demonstrate practical experience")
    
    # Skill-based suggestions
    if len(skills_detected) < 5:
        suggestions.append("Consider adding more technical skills to strengthen your profile")
    
    # ATS optimization suggestions
    if ats_score < 70:
        suggestions.append("Improve ATS optimization by adding more relevant keywords")
        suggestions.append("Use bullet points and proper formatting for better ATS parsing")
    
    # Content suggestions
    content_analysis = analyze_content_quality(text)
    suggestions.extend(content_analysis["suggestions"])
    
    return suggestions

def calculate_completeness_advanced(found_sections, skills_detected, ats_score):
    """Advanced completeness calculation"""
    section_score = len(found_sections) / len(SECTIONS)
    skill_score = min(len(skills_detected) / 15, 1.0)  # Cap at 15 skills
    ats_score_normalized = ats_score / 100
    
    # Weighted average
    completeness = (section_score * 0.4 + skill_score * 0.3 + ats_score_normalized * 0.3) * 100
    return round(completeness)

def simple_skill_extractor(text):
    """Legacy function for backward compatibility"""
    skills = advanced_skill_extractor(text)
    return {
        "skills_found": [skill["skill"] for skill in skills],
        "top_words": Counter(re.findall(r'\w+', text.lower())).most_common(20)
    }

def detect_sections(text):
    """Legacy function for backward compatibility"""
    return detect_sections_advanced(text)

def calculate_completeness(found_sections, skills_detected):
    """Legacy function for backward compatibility"""
    return calculate_completeness_advanced(found_sections, skills_detected, 50)
