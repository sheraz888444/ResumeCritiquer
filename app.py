"""Flask API for AI Resume Critiquer."""
import os
import io
import json
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI

load_dotenv()

app = Flask(__name__, static_folder=None, template_folder='.')
CORS(app)


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)


def extract_text_from_file(file):
    if file.filename.endswith('.pdf'):
        return extract_text_from_pdf(io.BytesIO(file.read()))
    return file.read().decode("utf-8")


def parse_ai_json(text):
    text = text.strip()
    # Try to find JSON in the text
    try:
        return json.loads(text)
    except:
        pass
    # Try finding JSON in code blocks
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return None


def build_analysis_prompt(resume_text, job_desc=None, role=None):
    role_ctx = role or "general job applications"
    job_section = ""
    if job_desc:
        job_section = "JOB DESCRIPTION (for match analysis):\n" + job_desc + "\n\n"
    
    prompt = """Analyze this resume and return a JSON object with the following structure. Return ONLY valid JSON, no other text.

""" + job_section + """TARGET ROLE: """ + role_ctx + """

RESUME CONTENT:
""" + resume_text + """

Return this exact JSON structure:

{
  "ats_score": 85,
  "ats_status": "Pass",
  "ats_breakdown": {
    "keywords": 90,
    "formatting": 80,
    "sections": 85,
    "readability": 85
  },
  "resume_summary": "Professional summary here",
  "skills": {
    "found_technical": ["Python", "JavaScript"],
    "found_soft": ["Communication"],
    "missing": ["SQL"]
  },
  "job_match": {
    "match_percentage": 75,
    "matching_keywords": ["Python"],
    "missing_keywords": ["SQL"],
    "skill_gap_analysis": "Some analysis"
  },
  "keywords": {
    "density_analysis": "Good density",
    "present": ["Python"],
    "missing": ["SQL"],
    "suggested": ["AWS"]
  },
  "experience": {
    "years": 5,
    "roles": ["Developer"],
    "career_progression": "Good progression"
  },
  "education": [
    {"degree": "BS Computer Science", "university": "University", "year": "2020", "relevance": "Relevant"}
  ],
  "formatting": {
    "file_type": "PDF",
    "tables_detected": false,
    "headings_ok": true,
    "graphics_issues": "None",
    "length_pages": 2,
    "issues": [],
    "compliant": true
  },
  "strengths": ["Good format"],
  "weaknesses": ["Missing keywords"],
  "improvements": ["Add more keywords"],
  "bonus_metrics": {
    "readability_score": 80,
    "length_score": 85,
    "grammar_score": 90,
    "section_completeness": 85
  }
}"""
    return prompt


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze')
@app.route('/analyze.html')
def analyze_page():
    return render_template('analyze.html')


@app.route('/about')
@app.route('/about.html')
def about_page():
    return render_template('about.html')


@app.route('/contact')
@app.route('/contact.html')
def contact_page():
    return render_template('contact.html')


@app.route('/privacy')
@app.route('/privacy.html')
def privacy_page():
    return render_template('privacy.html')


@app.route('/index.html')
def index_page():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    client = get_groq_client()
    
    if not client:
        return jsonify({"error": "GROQ_API_KEY not configured"}), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    job_description = request.form.get('job_description', '')
    job_role = request.form.get('job_role', '')
    
    try:
        file_content = extract_text_from_file(file)
        
        if not file_content.strip():
            return jsonify({"error": "File has no extractable content"}), 400
        
        prompt = build_analysis_prompt(
            file_content,
            job_description if job_description.strip() else None,
            job_role if job_role.strip() else None
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert ATS resume analyst. Return ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4000,
        )
        
        raw = response.choices[0].message.content
        data = parse_ai_json(raw)
        
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "Could not parse structured output", "raw": raw}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/contact', methods=['POST'])
def contact_form():
    data = request.get_json()
    return jsonify({"success": True, "message": "Thank you! Your message has been sent."})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
