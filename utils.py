"""Shared utilities for Resume Critiquer."""
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def render_top_navbar():
    """Render professional top navbar (sidebar hidden)."""
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        .stApp { background-color: #0d1117; }
        .nav-bar {
            background: linear-gradient(90deg, #21262d 0%, #30363d 50%, #21262d 100%);
            padding: 1.25rem 1.5rem;
            margin: -1rem -1rem 1.5rem -1rem;
            border-bottom: 3px solid #58a6ff;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            gap: 2rem;
            flex-wrap: wrap;
        }
        .nav-bar a {
            color: #e6edf3 !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
            text-decoration: none;
        }
        .nav-bar a:hover { color: #58a6ff !important; }
        .nav-brand { font-size: 1.2rem !important; }
    </style>
    <nav class="nav-bar">
        <a href="/" class="nav-brand">📃 AI Resume Critiquer</a>
        <a href="/">🏠 Home</a>
        <a href="/Analyze">📊 Analyze</a>
        <a href="/About">ℹ️ About</a>
        <a href="/Contact">📧 Contact</a>
        <a href="/Privacy_Policy">🔒 Privacy</a>
    </nav>
    """, unsafe_allow_html=True)

import io
import json
import re
import PyPDF2
from openai import OpenAI


def get_groq_client():
    """Get Groq API client."""
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
    if not api_key:
        return None, None
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1"), api_key


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)


def extract_text_from_file(uploaded_file):
    """Extract text from uploaded PDF or TXT file."""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")


def parse_ai_json(text: str) -> dict | None:
    """Extract and parse JSON from AI response. Handles markdown code blocks."""
    text = text.strip()
    # Remove markdown code blocks
    if "```json" in text:
        text = re.search(r"```json\s*([\s\S]*?)\s*```", text)
        text = text.group(1) if text else text
    elif "```" in text:
        text = re.search(r"```\s*([\s\S]*?)\s*```", text)
        text = text.group(1) if text else text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
