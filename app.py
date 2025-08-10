import streamlit as st
import pdfplumber
from question_generator import generate_questions
from speech_to_text import start_recording, stop_recording, full_process
from GLM_API import analyze_answer
from generate_user_profile_summary import generate_user_profile_summary

# --- Session state initialization ---
if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "num_questions" not in st.session_state:
    st.session_state.num_questions = 3
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = -1  # -1 means intro question
if "answers" not in st.session_state:
    st.session_state.answers = []
if "profile_summary" not in st.session_state:
    st.session_state.profile_summary = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""
if "start_msg" not in st.session_state:
    st.session_state.start_msg = ""
if "stop_msg" not in st.session_state:
    st.session_state.stop_msg = ""

st.title("🎤 AI Interviewer")

# --- Upload CV ---
cv_file = st.file_uploader("📄 Upload your CV (PDF only):", type=["pdf"])
if cv_file is not None:
    with pdfplumber.open(cv_file) as pdf:
        st.session_state.cv_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    st.success("CV uploaded and extracted successfully!")

# --- Job Description ---
st.session_state.job_description = st.text_area("💼 Enter Job Description:")

# --- Number of Technical Questions ---
st.session_state.num_questions = st.number_input(
    "❓ Number of technical questions:",
    min_value=1, max_value=10, value=3
)

# --- Introduce Yourself Step ---
if (
    st.session_state.cv_text
    and st.session_state.job_description
    and st.session_state.current_question_index == -1
    and len(st.session_state.answers) == 0
):
    st.markdown("## 🗣️ Question: Introduce yourself")

    # Reset messages when entering a new question
    st.session_state.start_msg = ""
    st.session_state.stop_msg = ""

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎤 Start Recording"):
            start_recording()
            st.session_state.start_msg = ":green[**▶ Recording started...**]"
            st.session_state.stop_msg = ""  # clear stop message
        if st.session_state.start_msg:
            st.markdown(st.session_state.start_msg)

    with col2:
        if st.button("🔕 Stop Recording"):
            filename = stop_recording()
            st.session_state.stop_msg = ":red[**⏹ Recording stopped**]"
            st.session_state.start_msg = ""  # clear start message
        if st.session_state.stop_msg:
            st.markdown(st.session_state.stop_msg)
            text = full_process(filename)
            st.session_state.answers.append(text)
            st.session_state.profile_summary = generate_user_profile_summary(
                st.session_state.cv_text,
                text
            )
            st.session_state.questions = generate_questions(
                st.session_state.job_description,
                st.session_state.num_questions,
                st.session_state.profile_summary
            )
            st.session_state.current_question_index = 0
        if st.session_state.stop_msg:
            st.session_state.stop_msg = ""  # clear stop message
            st.session_state.questions = generate_questions(
                st.session_state.job_description,
                st.session_state.num_questions,
                st.session_state.profile_summary
            )
            st.session_state.current_question_index = 0
        if st.session_state.stop_msg:
            st.markdown(st.session_state.stop_msg)

    # Show profile summary after answering intro question
    if st.session_state.profile_summary:
        st.subheader("📝 Profile Summary")
        st.write(st.session_state.profile_summary)

# --- Technical Questions ---
elif (
    st.session_state.current_question_index >= 0 and
    st.session_state.current_question_index < st.session_state.num_questions
):
    q_index = st.session_state.current_question_index
    question = st.session_state.questions[q_index]
    st.markdown(f"## 🗣️ Question {q_index + 1}: {question}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Start Recording", key=f"start_q{q_index}"):
            start_recording()
            st.session_state.start_msg = ":green[**▶ Recording started...**]"
            st.session_state.stop_msg = ""
    if st.session_state.start_msg:
        st.markdown(st.session_state.start_msg)

    with col2:
        if st.button("⏹️ Stop Recording", key=f"stop_q{q_index}"):
            filename = stop_recording()
            st.session_state.stop_msg = ":red[**⏹ Recording stopped**]"
            st.session_state.start_msg = ""
            if st.session_state.stop_msg:
                st.markdown(st.session_state.stop_msg)
            text = full_process(filename)
            st.session_state.answers.append(text)


    # Next button if answer recorded
    if len(st.session_state.answers) == q_index + 2:  # +1 for intro answer
        if st.session_state.current_question_index < st.session_state.num_questions - 1:
            if st.button("➡️ Next"):
                st.session_state.current_question_index += 1
        else:
            st.session_state.current_question_index += 1  # move to result

# --- Final Feedback ---
if st.session_state.current_question_index == st.session_state.num_questions:
    st.subheader("📊 Interview Analysis")
    if not st.session_state.analysis_result:
        with st.spinner("Analyzing your answers..."):
            st.session_state.analysis_result = analyze_answer(
                st.session_state.answers,
                st.session_state.job_description,
                st.session_state.profile_summary
            )
    st.text(st.session_state.analysis_result)
