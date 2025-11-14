import streamlit as st
import spacy

nlp = spacy.load("en_core_web_sm")

skills_list = [
    "python", "java", "sql", "machine learning", "deep learning", "data analysis",
    "django", "flask", "numpy", "pandas", "cloud computing", "aws", "docker",
    "communication", "team leadership"
]

def extract_skills(text):
    detected = set()
    for skill in skills_list:
        if skill.lower() in text.lower():
            detected.add(skill.title())
    return detected

st.title("🧠 AI Resume Skill Extractor")
st.write("Paste your resume text below and let the AI extract your skills!")

resume_text = st.text_area("Enter Resume Text")

if st.button("Extract Skills"):
    if resume_text.strip():
        skills = extract_skills(resume_text)
        if skills:
            st.success("🎯 Skills Found:")
            st.write(skills)
        else:
            st.warning("No skills detected.")
    else:
        st.error("Please enter resume text!")
