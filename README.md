# 🎙️ AI Interviewer

An interactive AI-powered interview assistant built with **Streamlit**.  
The application conducts a structured interview using voice input, generates questions based on the candidate's **CV**, **Job Description**, and **profile**, and provides a detailed AI-driven performance analysis at the end.

---

## 📌 Features

- **CV Upload & Parsing** – Extracts relevant information from the uploaded PDF CV.
- **Job Description Input** – Tailors the interview questions to match the provided JD.
- **Dynamic Question Generation**:
  - Starts with a fixed **"Introduce yourself"** question.
  - Generates technical questions based on the CV, JD, and user profile.
- **Voice Recording**:
  - Record answers directly from the browser.
  - Stop recording and convert speech to text.
- **User Profile Extraction** – Summarizes key details from the first answer to personalize upcoming questions.
- **Real-Time Feedback** – Displays recording status updates in the UI.
- **Comprehensive Final Analysis**:
  - Evaluates all answers with **Generative Language Models (GLM)**.
  - Produces a clear, bullet-pointed human-readable feedback report.

---

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit]()
- **Backend**:
  - Python 3.x
  - [pdfplumber](https://github.com/jsvine/pdfplumber) – for CV parsing
  - Custom question generation & user profiling
  - Speech-to-text processing
- **AI Models**:
  - **GLM (Generative Language Model)** – for question generation & answer analysis
  - Custom **Profile Summarization Model** – extracts candidate's name, skills, and relevant background from responses
- **Audio Handling**:
  - Browser-based recording
  - Automatic transcription and preprocessing (spelling correction, cleanup)

---

---

## ⚙️ How It Works

1. **Upload your CV** (PDF) and enter the job description.
2. **Set the number of technical questions** you want.
3. The interview starts with: **"Introduce yourself"**.
4. **Start Recording** → Answer the question → **Stop Recording**.
5. The first answer is analyzed to **generate your candidate profile**.
6. **AI generates tailored technical questions**.
7. For each question:
   - Record your answer
   - Stop and save
8. After all questions are answered:
   - The **GLM model** analyzes all answers
   - Generates a **clear, bullet-point feedback report** displayed in the UI.

---

## 🧠 Techniques Used

- **Natural Language Processing (NLP)**:
  - Text summarization for user profile
  - Contextual question generation
  - Sentiment & content-based evaluation of answers
- **Speech-to-Text**:
  - Automatic voice transcription
  - Preprocessing & error correction
- **Prompt Engineering**:
  - Structured prompts for GLM to ensure consistent output
- **Context-Aware AI**:
  - Combining CV, job description, and real-time user profile for tailored questions
- **Interactive UI Flow**:
  - Controlled question progression with a "Next" button
  - Live recording indicators
 ---

## 🎯 Conclusion

The **AI Interviewer** bridges the gap between traditional interviews and AI-driven assessment by offering a personalized, interactive, and insightful experience.  
By combining **speech recognition**, **NLP techniques**, and **context-aware question generation**, it not only simulates real interview scenarios but also provides actionable feedback for candidates to improve their performance.

Whether you're a job seeker preparing for your next opportunity or a developer exploring AI-powered applications, this project offers a practical and extendable solution that can be customized for various industries and interview formats.

---

