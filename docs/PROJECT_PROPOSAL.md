# Project Proposal: Resume–Job Match Scorer

**Author:** [Nahin Binte Wohab]  
**Course / term:** [AI Engineering Bootcamp for Programmers, Batch 3]  
**Repository:** [https://github.com/nahinbintewohab/Capstone-Project-Resume-Job-match-scorer-]


---

## 1. Problem statement

Job applicants often submit resumes without knowing how well they align with a specific posting. Manual comparison is slow and subjective; keyword-only tools miss paraphrasing; and generic advice does not reflect **this** job description. The problem is to give applicants a **quick, data-informed signal** (a match score) plus **actionable hints** (what to improve) using the actual text of their resume and the employer’s posting.

---

## 2. Proposed solution

A web application where the user **uploads a resume** (PDF or plain text) and **pastes a job description**. The system returns:

1. A **match score** from 0–100 combining lexical and semantic similarity.  
2. A short **summary** line and **improvement tips** derived from missing keywords and simple heuristics.

The same scoring pipeline is available in a **Google Colab notebook** for environments where local install is not possible.

---

## 3. AI approach

- **Sentence embeddings:** Text is encoded with **`all-MiniLM-L6-v2`** via the `sentence-transformers` library. Embeddings capture meaning beyond exact word matches.  
- **Semantic score:** **Cosine similarity** between resume and job embeddings; scaled to a 0–100 sub-score.  
- **Keyword score:** Overlap of informative words (with light stopword filtering) between resume and job; scaled to 0–100.  
- **Hybrid fusion:** Final score = **40% keyword + 60% semantic** to balance “must-have terms” with overall topical fit.  
- **Tips:** Rule-based suggestions (e.g., job terms missing from the resume); optional future work: LLM summarization or OpenAI embeddings.

No user data is assumed to be retained for training; inference only.

---

## 4. Tech stack

| Area | Technology |
|------|------------|
| Frontend | React 18, Vite, HTML/CSS |
| Backend | Python 3.11, FastAPI, Uvicorn |
| PDF parsing | PyPDF2 |
| ML / NLP | sentence-transformers, PyTorch (via dependency), NumPy |
| Local dev | Two processes: API on port 8000, UI on 5173 (Vite proxy) |
| Deployment | **Frontend:** Vercel · **Backend:** Render (Web Service) |
| Alternative run | Jupyter notebook on Google Colab |

---

## 5. Success criteria 

- [ ] End-to-end flow: upload + paste → score + tips.  
- [ ] Public deployment: live URL for UI and working API.  
- [ ] Documentation: README with setup, methodology, and usage.

---


