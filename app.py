import os
import io
import streamlit as st
import spacy
import en_core_web_sm
from spacy.matcher import PhraseMatcher
from PyPDF2 import PdfReader

# Load spaCy model (recommended for Render after installing model as package)
nlp = en_core_web_sm.load()

# Skill list (expand as you like)
skills_list = [
    "python", "java", "sql", "machine learning", "deep learning", "data analysis",
    "django", "flask", "numpy", "pandas", "cloud computing", "aws", "azure", "gcp",
    "docker", "kubernetes", "communication", "team leadership", "tensorflow", "pytorch",
    "nlp", "computer vision", "html", "css", "javascript"
]

# Build PhraseMatcher for multi-word skills (case-insensitive)
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in skills_list]
matcher.add("SKILLS", patterns)


def extract_text_from_pdf(file_bytes):
    """Extract text from uploaded PDF file bytes"""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n".join(pages)
    except Exception:
        return ""


def extract_skills(text):
    """Extract skills using PhraseMatcher & fallback substring matching"""
    doc = nlp(text or "")
    found = set()

    # PhraseMatcher matches (stronger for multi-word skills)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        found.add(span.text.title())

    # Fallback substring check to catch single-word mentions or synonyms
    lowered = text.lower()
    for skill in skills_list:
        if skill.lower() in lowered:
            found.add(skill.title())

    return sorted(found)


# Streamlit UI
st.set_page_config(page_title="AI Resume Skill Extractor", layout="centered")
st.title("🧠 AI Resume Skill Extractor")
st.write("Paste resume text or upload a PDF to extract technical & soft skills.")

# Option: paste text
resume_text = st.text_area("Paste resume text here", height=200)

# Option: upload PDF
uploaded_file = st.file_uploader("Or upload a resume (PDF)", type=["pdf"])
if uploaded_file is not None:
    raw = uploaded_file.read()
    pdf_text = extract_text_from_pdf(raw)
    if pdf_text:
        # if user didn't paste text, populate the text area (but do not overwrite if user pasted)
        if not resume_text.strip():
            resume_text = pdf_text
            st.info("Text extracted from PDF and placed into the text box above. You may edit it before extracting.")

if st.button("Extract Skills"):
    if not resume_text.strip():
        st.error("Please paste resume text or upload a PDF first.")
    else:
        with st.spinner("Extracting skills..."):
            skills = extract_skills(resume_text)
        if skills:
            st.success(f"🎯 Skills Found ({len(skills)}):")
            # display as badges-like UI
            cols = st.columns(3)
            for i, skill in enumerate(skills):
                cols[i % 3].markdown(f"- **{skill}**")
        else:
            st.warning("No skills detected. Try adding more resume content or spelling out abbreviations (e.g., 'AWS').")

st.markdown("---")
st.caption("Built with spaCy & Streamlit — deployable to Render. Expand `skills_list` to improve coverage.")
