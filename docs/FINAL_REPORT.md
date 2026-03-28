# Final Report: Resume–Job Match Scorer

**Author:** Nahin Binte Wohab
**Course / term:** [AI Engineering Bootcamp for Programmers, Batch 3]  
**Repository:** [https://github.com/nahinbintewohab/Capstone-Project-Resume-Job-match-scorer-]  
**Live application:** [https://capstone-project-resume-job-match-s.vercel.app/] · **API:** [Render `/docs` https://resume-job-match-scorer-gxyo.onrender.com/]



---

## 1. Problem solved

Summarize the applicant’s pain point: uncertainty about fit, time cost of manual review, and limitations of pure keyword screening. State the goal: **quantified match score** plus **concrete improvement tips** driven by the actual job text and resume.

---

## 2. Design decisions

### 2.1 Architecture

- **Split deployment:** React static frontend (Vercel) + Python API with ML stack (Render). Rationale: serverless frontend hosts are ill-suited to large PyTorch bundles and long cold starts on the same bundle as the UI.  
- **REST API:** `POST /api/analyze` with multipart upload keeps the browser simple and matches OpenAPI/Swagger tooling for graders and testers.

### 2.2 Hybrid scoring

- **Why not semantic-only?** Job descriptions often list **must-have tools and credentials**; embedding similarity alone can underweight exact skill tokens.  
- **Why not keyword-only?** Synonyms and paraphrases (“led a team” vs “managed people”) matter; embeddings capture that.  
- **Weights:** 40% keyword / 60% semantic is a starting compromise; [describe any tuning or user feedback you collected].

### 2.3 Tips

- **Rule-based tips** keep latency and cost low and avoid extra API keys. Trade-off: less fluent than an LLM; [note if you tested alternatives].

### 2.4 PDF handling

- **PyPDF2** for text extraction; limitation: complex layouts or scans may yield poor text—[mention if you observed failures].

---

## 3. AI workflow (end-to-end)

1. User uploads resume file; server reads bytes.  
2. If PDF: extract text per page; else decode as UTF-8 text.  
3. Normalize and slice long texts if needed for embedding input caps.  
4. Compute **keyword score** from token sets (stopword filtering).  
5. Load **SentenceTransformer(`all-MiniLM-L6-v2`)** (lazy-loaded once per process on the server).  
6. Encode resume and job text; **cosine similarity** → semantic sub-score.  
7. Blend scores; generate **tips** from set differences and simple rules.  
8. Return JSON to the UI for display.

Include a **diagram** if your course requires it (flowchart or sequence diagram).

---

## 4. Implementation summary

| Component | Path | Role |
|-----------|------|------|
| API | `backend/main.py` | FastAPI routes, CORS, scoring |
| Dependencies | `backend/requirements.txt` | Pins compatible versions (incl. Python 3.11 on Render) |
| UI | `frontend/src/App.jsx` | Upload, form, fetch, results |
| Notebook | `colab/resume_job_match_colab.ipynb` | Same logic without server |

---

## 5. Results


- Example job families tested (e.g., data analyst, software engineer).  
- Whether scores **ranked** obviously better/worse resumes as expected (qualitative).  
- **Failure cases:** scanned PDFs, very short job posts, non-English text.  
- **Latency:** local vs cold start on Render; model load time on first request.  

---

## 6. Ethics and limitations

- Scores are **assistive**, not hiring decisions; bias in postings or resumes is not corrected by this baseline system.    
- Free tiers: sleep, timeouts, and rate limits affect demos.

---

## 7. Conclusions

This project delivered a **complete, deployable pipeline** from raw resume files and job text to a **numeric match score** and **human-readable improvement tips**. The main technical bet—that a **hybrid of keyword overlap and sentence embeddings** would be more useful than either method alone—proved sound in practice: embeddings capture paraphrase and topical similarity, while the lexical component keeps the score sensitive to concrete skills and terms that employers repeat in postings. Splitting the **React frontend** and **FastAPI ML backend** across **Vercel** and **Render** respectively was a necessary design response to the size of the transformer stack and to cold-start behavior on free hosting, not merely an implementation detail.

The system remains deliberately **modest in scope**: tips are rule-based rather than LLM-generated, PDF extraction is brittle on scans or exotic layouts, and a single generic English model is not tuned to every industry or locale. These limits are acceptable for a capstone prototype but point to natural extensions—OCR for scanned resumes, multilingual or domain-fine-tuned embeddings, optional LLM summaries, and small user studies to validate whether scores track human intuition.

Overall, the work satisfies the core objectives: it **solves a real applicant problem** with **transparent AI components** (documented model choice and scoring math), ships as **working code with clear commits and documentation**, and is **accessible online** through standard cloud tooling. The result is a credible foundation that could evolve into a richer career-coaching product, while already demonstrating proficiency in full-stack integration, applied NLP, and responsible framing of automated scoring as guidance rather than judgment.

---

## References

- Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* (Underlying family of models; see sentence-transformers model card for `all-MiniLM-L6-v2`.)  
- FastAPI: https://fastapi.tiangolo.com/  
- Sentence Transformers: https://www.sbert.net/

---

