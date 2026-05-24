import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from google import genai
from PIL import Image
from PyPDF2 import PdfReader
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import tempfile
import os

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
vision_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="JZP_AI OS", page_icon="🚀", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right,#020617,#0f172a);
    color: white;
}
.hero {
    font-size: 55px;
    font-weight: bold;
    background: linear-gradient(90deg,#a855f7,#3b82f6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.card {
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    padding:20px;
    border-radius:20px;
}
.chat-user {
    background: rgba(59,130,246,0.15);
    padding:15px;
    border-radius:15px;
    margin-bottom:10px;
}
.chat-ai {
    background: rgba(168,85,247,0.15);
    padding:15px;
    border-radius:15px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🚀 JZP_AI OS")
    st.caption("Future AI Operating System")

    page = st.radio(
        "Navigation",
        [
            "💬 AI Chat",
            "🎤 Voice AI",
            "🖼 Vision AI",
            "📄 PDF AI",
            "📑 Resume Analyzer",
            "💻 Code Generator"
        ]
    )

    st.divider()

    st.markdown("""
    ### Features
    ✅ AI Chat
    ✅ Voice AI
    ✅ Gemini Vision
    ✅ PDF Summary
    ✅ Resume Analysis
    ✅ AI Code Generator
    """)

st.markdown('<p class="hero">JZP_AI OS</p>', unsafe_allow_html=True)
st.subheader("Next Generation AI Platform")

c1,c2,c3,c4 = st.columns(4)

cards = [
    ("🤖 AI Chat","Smart assistant"),
    ("🎤 Voice AI","Talk with AI"),
    ("🖼 Vision AI","Analyze images"),
    ("📄 PDF AI","Summarize PDFs")
]

for col, card in zip([c1,c2,c3,c4], cards):
    with col:
        st.markdown(f"""
        <div class="card">
        <h3>{card[0]}</h3>
        <p>{card[1]}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

if page == "💬 AI Chat":

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><b>🧑 You</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai"><b>🤖 AI</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Ask anything...")

    if prompt:

        st.session_state.messages.append({
            "role":"user",
            "content":prompt
        })

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_reply = response.choices[0].message.content

        st.session_state.messages.append({
            "role":"assistant",
            "content":ai_reply
        })

        st.rerun()

elif page == "🎤 Voice AI":

    st.markdown("## 🎤 Voice Assistant")

    audio_bytes = audio_recorder()

    if audio_bytes:

        st.audio(audio_bytes, format="audio/wav")

        user_prompt = st.text_input("Type what you said")

        if st.button("🚀 Ask AI"):

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"user",
                        "content":user_prompt
                    }
                ]
            )

            ai_reply = response.choices[0].message.content

            st.write(ai_reply)

            tts = gTTS(ai_reply)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:

                tts.save(fp.name)

                audio_file = open(fp.name, "rb")

                st.audio(audio_file.read(), format="audio/mp3")

elif page == "🖼 Vision AI":

    st.markdown("## 🖼 Upload Image")

    image_file = st.file_uploader(
        "Upload Image",
        type=["png","jpg","jpeg"]
    )

    if image_file:

        image = Image.open(image_file)

        st.image(image, use_container_width=True)

        prompt = st.text_input(
            "Ask about the image",
            value="Describe this image in detail"
        )

        if st.button("🚀 Analyze Image"):

            response = vision_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, image]
            )

            st.markdown("## 📌 AI Analysis")
            st.write(response.text)

elif page == "📄 PDF AI":

    pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if pdf:

        reader = PdfReader(pdf)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        if st.button("✨ Summarize PDF"):

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"user",
                        "content":f"Summarize this PDF:\\n\\n{text[:12000]}"
                    }
                ]
            )

            summary = response.choices[0].message.content

            st.markdown("## 📄 Summary")
            st.write(summary)

elif page == "📑 Resume Analyzer":

    resume = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    if resume:

        reader = PdfReader(resume)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        if st.button("📊 Analyze Resume"):

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"user",
                        "content":f"Analyze this resume and give strengths, weaknesses, ATS score and improvements.\\n\\n{text[:12000]}"
                    }
                ]
            )

            result = response.choices[0].message.content

            st.markdown("## 🚀 Analysis")
            st.write(result)

else:

    prompt = st.text_area("Describe code you want")

    if st.button("⚡ Generate Code"):

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"user",
                    "content":f"Generate clean code for:\\n{prompt}"
                }
            ]
        )

        code = response.choices[0].message.content

        st.code(code)
