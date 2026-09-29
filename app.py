import re
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


st.set_page_config(
    page_title="PrepX AI",
    page_icon="🎯",
    layout="wide",
)

SKILLS = [
    "python", "java", "c", "c++", "sql", "mongodb", "machine learning",
    "deep learning", "nlp", "pytorch", "tensorflow", "scikit-learn",
    "git", "github", "docker", "aws", "azure", "gcp", "react",
    "javascript", "typescript", "data structures", "algorithms",
    "oop", "computer networks", "operating systems", "dbms"
]

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you",
    "are", "will", "have", "has", "our", "into", "their", "they", "job",
    "role", "work", "using", "use", "years", "year", "about", "skills"
}


def extract_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    data = uploaded_file.read()
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        if fitz is None:
            return "PDF support requires PyMuPDF."
        doc = fitz.open(stream=data, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    return data.decode("utf-8", errors="ignore")


def extract_skills(text: str) -> List[str]:
    low = text.lower()
    found = []
    for skill in SKILLS:
        if skill in low:
            found.append(skill)
    return sorted(set(found))


def keyword_overlap(resume: str, jd: str) -> Tuple[List[str], List[str]]:
    r = set(extract_skills(resume))
    j = set(extract_skills(jd))
    return sorted(r & j), sorted(j - r)


def tokenize(text: str) -> List[str]:
    return [
        w for w in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower())
        if w not in STOPWORDS
    ]


def top_terms(text: str, n=12) -> List[str]:
    freq = {}
    for w in tokenize(text):
        freq[w] = freq.get(w, 0) + 1
    return [x for x, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:n]]


def build_questions(common: List[str], gaps: List[str]) -> List[str]:
    questions = [
        "Tell me about yourself and the kind of role you are targeting.",
        "Walk me through one project where you solved a difficult technical problem.",
        "Describe a time you made a trade-off between speed and quality.",
    ]
    for skill in common[:3]:
        questions.append(f"Explain a project where you used {skill}. What did you personally implement?")
    for skill in gaps[:3]:
        questions.append(f"The role asks for {skill}. How would you learn or apply it in your first 30 days?")
    return questions[:8]


def evaluate_answer(answer: str, question: str) -> Dict:
    words = tokenize(answer)
    low = answer.lower()
    filler = sum(low.count(x) for x in [" um ", " uh ", " like ", " basically ", " actually "])
    has_example = any(x in low for x in ["project", "example", "built", "implemented", "created", "developed"])
    has_result = any(x in low for x in ["result", "improved", "reduced", "increased", "%", "impact"])
    length_score = min(10, max(2, len(words) / 12))
    structure = 2 + int(has_example) * 4 + int(has_result) * 3
    relevance = 8 if any(q in low for q in tokenize(question)[:3]) else 6
    clarity = max(1, 10 - min(6, filler))
    return {
        "overall": round(min(10, (length_score + structure + relevance + clarity) / 4), 1),
        "length": len(words),
        "filler_count": filler,
        "example": has_example,
        "result": has_result,
        "clarity": clarity,
    }


# This is the reference/demo engine. Replace this adapter with a Qualcomm AI Hub
# QNN/Genie/QAIRT-backed local model on a supported Snapdragon device.
class LocalCoachEngine:
    name = "Reference Local Engine (CPU)"

    def generate_feedback(self, question: str, answer: str) -> Dict:
        return evaluate_answer(answer, question)


st.title("🎯 PrepX AI")
st.caption("Private-by-design interview coaching • Snapdragon-ready architecture")

with st.sidebar:
    st.header("Privacy")
    st.success("Reference demo processes your text locally.")
    st.info("No cloud API is used by this demo.")
    st.header("Engine")
    st.code(LocalCoachEngine.name)

tab1, tab2, tab3 = st.tabs(["🧩 Resume + JD", "🎤 Mock Interview", "📊 Report"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Resume")
        resume_file = st.file_uploader("Upload TXT/PDF", type=["txt", "pdf"])
        resume_text = st.text_area(
            "Or paste resume text",
            value=st.session_state.get("resume_text", ""),
            height=300,
        )
        if resume_file:
            resume_text = extract_text(resume_file)
            st.session_state["resume_text"] = resume_text
    with c2:
        st.subheader("Job Description")
        jd_text = st.text_area(
            "Paste the job description",
            value=st.session_state.get("jd_text", ""),
            height=300,
        )
        st.session_state["jd_text"] = jd_text

    if st.button("Analyze fit", type="primary", use_container_width=True):
        common, gaps = keyword_overlap(resume_text, jd_text)
        st.session_state["common"] = common
        st.session_state["gaps"] = gaps
        st.session_state["questions"] = build_questions(common, gaps)

    if "common" in st.session_state:
        common = st.session_state["common"]
        gaps = st.session_state["gaps"]
        st.subheader("Role fit snapshot")
        a, b, c = st.columns(3)
        a.metric("Matched skills", len(common))
        b.metric("Skill gaps", len(gaps))
        c.metric("Questions", len(st.session_state["questions"]))

        st.write("**Matched:** " + (", ".join(common) if common else "None detected"))
        st.write("**Gaps to prepare:** " + (", ".join(gaps) if gaps else "None detected"))

        st.subheader("Personalized question set")
        for i, q in enumerate(st.session_state["questions"], 1):
            st.write(f"**{i}.** {q}")

with tab2:
    st.subheader("Mock interview")
    if "questions" not in st.session_state:
        st.warning("First analyze a resume + job description.")
    else:
        qs = st.session_state["questions"]
        idx = st.number_input("Question", min_value=1, max_value=len(qs), value=1) - 1
        q = qs[idx]
        st.info(q)
        answer = st.text_area("Your answer", height=220, placeholder="Answer as if you are in the interview...")
        if st.button("Evaluate answer", type="primary"):
            feedback = LocalCoachEngine().generate_feedback(q, answer)
            st.session_state["last_feedback"] = feedback
            st.session_state["last_question"] = q
            st.session_state["last_answer"] = answer

        if "last_feedback" in st.session_state:
            f = st.session_state["last_feedback"]
            st.metric("Demo score", f"{f['overall']}/10")
            st.write(f"**Answer length:** {f['length']} words")
            st.write(f"**Clarity indicator:** {f['clarity']}/10")
            st.write(f"**Example included:** {'Yes' if f['example'] else 'No'}")
            st.write(f"**Result/impact included:** {'Yes' if f['result'] else 'No'}")
            st.write(f"**Detected filler words:** {f['filler_count']}")

            tips = []
            if not f["example"]:
                tips.append("Add one concrete project or real-world example.")
            if not f["result"]:
                tips.append("End with measurable impact, result, or learning.")
            if f["length"] < 45:
                tips.append("Expand the answer using Situation → Task → Action → Result.")
            if f["length"] > 180:
                tips.append("Tighten the answer and keep the main story focused.")
            if not tips:
                tips.append("Good structure. Practice delivering the answer naturally without memorizing it.")
            st.write("**Next improvements:**")
            for tip in tips:
                st.write("• " + tip)

with tab3:
    st.subheader("Preparation report")
    if "resume_text" not in st.session_state or not st.session_state.get("resume_text"):
        st.info("Analyze a resume + JD to create the report.")
    else:
        common = st.session_state.get("common", [])
        gaps = st.session_state.get("gaps", [])
        st.write("### Candidate strengths")
        for x in common[:8]:
            st.write("• " + x)
        st.write("### Priority preparation areas")
        for x in gaps[:8]:
            st.write("• " + x)
        st.write("### Interview strategy")
        st.write("• Prepare 2 STAR stories from your strongest projects.")
        st.write("• For every technical skill, prepare one implementation example.")
        st.write("• Quantify impact wherever possible.")
        st.write("• Keep a 60–90 second introduction ready.")
        st.write("• Practice aloud; voice mode can be connected to a local Whisper adapter.")

st.divider()
st.caption("PrepX AI is an independent prototype for the Qualcomm Snapdragon AI Lab Build & Present Challenge. Snapdragon and Qualcomm are trademarks of Qualcomm Incorporated or its subsidiaries.")
