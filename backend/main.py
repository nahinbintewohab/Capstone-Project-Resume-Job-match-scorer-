"""
Resume–Job Match Scorer API
- Accept resume (PDF) + job description
- Return match score (0–100) and improvement tips
- Uses sentence-transformers for semantic similarity; optional keyword boost
"""
import io
import os
import re
_origins = os.environ.get("FRONTEND_ORIGIN", "*").strip()
_cors_origins = [o.strip() for o in _origins.split(",") if o.strip()] if _origins != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,

from typing import List, Optional

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Lazy-load heavy deps to speed startup on Render
def get_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(content: bytes) -> str:
    import PyPDF2
    reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip() or ""

app = FastAPI(title="Resume–Job Match Scorer API")

# CORS: set FRONTEND_ORIGIN on Render to your Vercel URL (e.g. https://your-app.vercel.app). Comma-separate multiple.
_origins = os.environ.get("FRONTEND_ORIGIN", "*").strip()
_cors_origins = [o.strip() for o in _origins.split(",") if o.strip()] if _origins != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,  # must be False when using allow_origins=["*"]; fine for this API (no cookies)
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache for model (avoids reload on each request)
_embedder = None

def embedder():
    global _embedder
    if _embedder is None:
        _embedder = get_embedder()
    return _embedder

class AnalyzeResponse(BaseModel):
    score: float
    tips: List[str]
    summary: Optional[str] = None

def keyword_score(resume_lower: str, job_lower: str) -> float:
    """Simple keyword overlap: required skills often appear after 'required', 'skills', 'experience'."""
    # Extract words from job description (skip very common words)
    stop = {"the", "and", "for", "with", "or", "to", "in", "of", "a", "an", "is", "on", "at"}
    job_words = set(re.findall(r"\b[a-z]{3,}\b", job_lower)) - stop
    resume_words = set(re.findall(r"\b[a-z]{3,}\b", resume_lower))
    if not job_words:
        return 50.0
    overlap = len(job_words & resume_words) / len(job_words)
    return min(100.0, overlap * 100)

def semantic_score(resume_text: str, job_text: str) -> float:
    """Cosine similarity between embeddings, scaled to 0–100."""
    model = embedder()
    # Use first 512 tokens worth of text to avoid overflow
    r = resume_text[:4000] if len(resume_text) > 4000 else resume_text
    j = job_text[:4000] if len(job_text) > 4000 else job_text
    embs = model.encode([r, j])
    import numpy as np
    sim = np.dot(embs[0], embs[1]) / (np.linalg.norm(embs[0]) * np.linalg.norm(embs[1]) + 1e-9)
    # Map [-1,1] to [0,100]
    return float((sim + 1) * 50)

def generate_tips(resume_text: str, job_text: str, score: float) -> List[str]:
    tips = []
    resume_lower = resume_text.lower()
    job_lower = job_text.lower()
    # Keywords from job that might be missing
    job_words = set(re.findall(r"\b[a-z]{4,}\b", job_lower))
    resume_words = set(re.findall(r"\b[a-z]{4,}\b", resume_lower))
    missing = job_words - resume_words
    # Suggest adding a few high-value missing terms if score is low
    if score < 70 and missing:
        sample = list(missing)[:5]
        tips.append(f"Consider adding these terms from the job description: {', '.join(sample)}.")
    if score < 60:
        tips.append("Expand your experience section to better align with the job responsibilities.")
    if "experience" in job_lower and "experience" not in resume_lower and "work" not in resume_lower:
        tips.append("Add a clear 'Experience' or 'Work History' section.")
    if not tips:
        tips.append("Your resume is well aligned with this job. Consider tailoring the summary to this role.")
    return tips[:5]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(""),
):
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="job_description is required")

    content = await resume.read()
    if resume.filename and resume.filename.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(content)
    else:
        resume_text = content.decode("utf-8", errors="replace")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from resume")

    job_text = job_description.strip()

    kw = keyword_score(resume_text, job_text)
    sem = semantic_score(resume_text, job_text)
    score = round(0.4 * kw + 0.6 * sem, 1)

    tips = generate_tips(resume_text, job_text, score)
    summary = f"Match: {score}/100 (keyword + semantic). " + ("Strong fit." if score >= 70 else "Consider the tips below.")

    return AnalyzeResponse(score=score, tips=tips, summary=summary)
