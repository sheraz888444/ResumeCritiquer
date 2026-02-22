"""AI Resume Analysis page with professional ATS-focused results."""
import streamlit as st
from utils import get_groq_client, extract_text_from_file, parse_ai_json, render_top_navbar

st.set_page_config(page_title="Analyze Resume | AI Resume Critiquer", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
render_top_navbar()

# Custom styles for analysis results
st.markdown("""
<style>
    .ats-score-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #2d5a87;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .ats-score-number { font-size: 3.5rem; font-weight: 700; color: #4fc3f7; }
    .ats-pass { color: #4caf50; }
    .ats-fail { color: #f44336; }
    .ats-moderate { color: #ff9800; }
    .section-card {
        background: #1a2634;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #2d5a87;
    }
    .skill-found { color: #4caf50; }
    .skill-missing { color: #f44336; }
    .progress-bar-container {
        background: #0d2137;
        border-radius: 8px;
        height: 12px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)


st.title("📊 AI Resume Analysis")
st.markdown("Upload your resume and get professional ATS-focused feedback with actionable insights.")

client, api_key = get_groq_client()

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"], key="resume_upload")
job_description = st.text_area("Paste Job Description (optional - for Resume vs Job Match analysis)", height=120, key="job_desc")
job_role = st.text_input("Target job role (optional)", key="job_role", placeholder="e.g., Frontend Developer")

analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)


def build_analysis_prompt(resume_text: str, job_desc: str | None, role: str | None) -> str:
    """Build comprehensive prompt for structured resume analysis."""
    role_ctx = role or "general job applications"
    job_section = ""
    if job_desc:
        job_section = f"""
JOB DESCRIPTION (for match analysis):
{job_desc}

"""
    return f"""Analyze this resume and return a JSON object with the following structure. Return ONLY valid JSON, no other text.

{job_section}TARGET ROLE: {role_ctx}

RESUME CONTENT:
{resume_text}

Return this exact JSON structure (use null for job_match if no job description provided):

{{
  "ats_score": <number 0-100>,
  "ats_status": "<Pass|Moderate|Needs Improvement|Fail>",
  "ats_breakdown": {{
    "keywords": <0-100>,
    "formatting": <0-100>,
    "sections": <0-100>,
    "readability": <0-100>
  }},
  "resume_summary": "<4-6 line professional summary of the candidate>",
  "skills": {{
    "found_technical": ["skill1", "skill2"],
    "found_soft": ["skill1", "skill2"],
    "missing": ["skill1", "skill2"]
  }},
  "job_match": {{
    "match_percentage": <0-100>,
    "matching_keywords": ["kw1", "kw2"],
    "missing_keywords": ["kw1", "kw2"],
    "skill_gap_analysis": "<brief analysis>"
  }}  OR null if no job description,
  "keywords": {{
    "density_analysis": "<brief analysis>",
    "present": ["kw1", "kw2"],
    "missing": ["kw1", "kw2"],
    "suggested": ["kw1", "kw2"]
  }},
  "experience": {{
    "years": <number or float>,
    "roles": ["role1", "role2"],
    "career_progression": "<brief analysis>"
  }},
  "education": [
    {{"degree": "...", "university": "...", "year": "...", "relevance": "..."}}
  ],
  "formatting": {{
    "file_type": "PDF or TXT",
    "tables_detected": true/false,
    "headings_ok": true/false,
    "graphics_issues": "<description or None>",
    "length_pages": <estimated pages>,
    "issues": ["issue1", "issue2"],
    "compliant": true/false
  }},
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "improvements": ["suggestion1", "suggestion2"],
  "bonus_metrics": {{
    "readability_score": <0-100>,
    "length_score": <0-100>,
    "grammar_score": <0-100>,
    "section_completeness": <0-100>
  }}
}}"""


def render_results(data: dict):
    """Render analysis results in professional layout."""
    # 1. ATS Score
    score = data.get("ats_score", 0)
    status = data.get("ats_status", "Unknown")
    status_class = "ats-pass" if "Pass" in status else ("ats-fail" if "Fail" in status else "ats-moderate")
    breakdown = data.get("ats_breakdown", {})

    st.markdown(f"""
    <div class="ats-score-card">
        <p style="color:#90a4ae; margin:0 0 0.5rem 0;">ATS Compatibility Score</p>
        <p class="ats-score-number">{score}<span style="font-size:1.5rem; color:#90a4ae;">/100</span></p>
        <p class="{status_class}" style="font-size:1.2rem; font-weight:600;">Status: {status}</p>
        <div style="margin-top:1.5rem; text-align:left; max-width:400px; margin-left:auto; margin-right:auto;">
            {"".join(f'<div><small>{k.title()}: </small><div class="progress-bar-container"><div class="progress-bar-fill" style="width:{v}%; background:linear-gradient(90deg,#2d5a87,#4fc3f7);"></div></div></div>' for k,v in breakdown.items())}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Resume Summary
    summary = data.get("resume_summary", "")
    if summary:
        st.markdown("### 📝 AI Resume Insights")
        st.markdown(f'<div class="section-card"><p style="margin:0; line-height:1.6;">{summary}</p></div>', unsafe_allow_html=True)

    # 3. Skills Analysis
    skills = data.get("skills", {})
    if skills:
        st.markdown("### 🧩 Skill Gap Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            found = skills.get("found_technical", []) + skills.get("found_soft", [])
            st.markdown("**✔ Found Skills**")
            st.markdown(", ".join(found) if found else "—")
        with col2:
            missing = skills.get("missing", [])
            st.markdown("**❌ Missing Skills**")
            st.markdown(", ".join(missing) if missing else "None identified")
        with col3:
            st.markdown("**Key Strengths**")
            st.markdown(f"Technical: {len(skills.get('found_technical', []))} | Soft: {len(skills.get('found_soft', []))}")

    # 4. Resume vs Job Match
    job_match = data.get("job_match")
    if job_match:
        st.markdown("### ⭐ Resume vs Job Description Match")
        match_pct = job_match.get("match_percentage", 0)
        st.progress(match_pct / 100)
        st.markdown(f"**Match: {match_pct}%**")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown("**Matching keywords:** " + ", ".join(job_match.get("matching_keywords", []) or ["—"]))
        with m2:
            st.markdown("**Missing keywords:** " + ", ".join(job_match.get("missing_keywords", []) or ["—"]))
        if job_match.get("skill_gap_analysis"):
            st.info(job_match["skill_gap_analysis"])

    # 5. Keyword Optimization
    keywords = data.get("keywords", {})
    if keywords:
        st.markdown("### 🔑 Keyword Match Analysis")
        st.caption(keywords.get("density_analysis", ""))
        k1, k2 = st.columns(2)
        with k1:
            st.markdown("**✔ Present:** " + ", ".join(keywords.get("present", []) or ["—"]))
        with k2:
            st.markdown("**❌ Missing / Suggested:** " + ", ".join((keywords.get("missing", []) or []) + (keywords.get("suggested", []) or [])))

    # 6. Experience Analysis
    exp = data.get("experience", {})
    if exp:
        st.markdown("### 💼 Experience Analysis")
        st.markdown(f"**Detected Experience:** {exp.get('years', 'N/A')} years")
        st.markdown("**Roles:** " + ", ".join(exp.get("roles", []) or ["—"]))
        if exp.get("career_progression"):
            st.caption(exp["career_progression"])

    # 7. Education Analysis
    education = data.get("education", [])
    if education:
        st.markdown("### 🎓 Education Analysis")
        for ed in education:
            if isinstance(ed, dict):
                st.markdown(f"- **{ed.get('degree', '')}** — {ed.get('university', '')} ({ed.get('year', '')})")
                if ed.get("relevance"):
                    st.caption(ed["relevance"])

    # 8. Formatting & ATS Compliance
    fmt = data.get("formatting", {})
    if fmt:
        st.markdown("### 📄 Formatting & ATS Compliance Check")
        compliant = fmt.get("compliant", False)
        st.markdown(f"**Status:** {'✔ ATS Friendly' if compliant else '⚠ Needs attention'}")
        st.markdown(f"File type: {fmt.get('file_type', '—')} | Length: ~{fmt.get('length_pages', '—')} page(s)")
        if fmt.get("headings_ok") is not None:
            st.markdown("Section headings: " + ("✔ OK" if fmt["headings_ok"] else "❌ Improve"))
        for issue in fmt.get("issues", []) or []:
            st.markdown(f"- ⚠ {issue}")

    # 9. Strengths & Weaknesses
    strengths = data.get("strengths", [])
    weaknesses = data.get("weaknesses", [])
    if strengths or weaknesses:
        st.markdown("### 📈 AI Insights: Strengths & Weaknesses")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Strengths**")
            for s in strengths:
                st.markdown(f"- ✔ {s}")
        with c2:
            st.markdown("**Weaknesses**")
            for w in weaknesses:
                st.markdown(f"- ❌ {w}")

    # 10. Improvement Suggestions
    improvements = data.get("improvements", [])
    if improvements:
        st.markdown("### 🎯 Optimization Recommendations")
        for i, imp in enumerate(improvements, 1):
            st.markdown(f"{i}. {imp}")

    # Bonus metrics
    bonus = data.get("bonus_metrics", {})
    if bonus:
        st.markdown("### 💎 Additional Metrics")
        b1, b2, b3, b4 = st.columns(4)
        for col, (label, val) in zip([b1, b2, b3, b4], [
            ("Readability Score", bonus.get("readability_score")),
            ("Length Score", bonus.get("length_score")),
            ("Grammar Score", bonus.get("grammar_score")),
            ("Section Completeness", bonus.get("section_completeness")),
        ]):
            with col:
                if val is not None:
                    st.metric(label, f"{val}/100", "")


if analyze_btn and uploaded_file:
    if not api_key:
        st.error("Please set GROQ_API_KEY in your .env file (get free key at https://console.groq.com).")
        st.stop()

    try:
        with st.spinner("Analyzing your resume with AI..."):
            file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File has no extractable content.")
            st.stop()

        prompt = build_analysis_prompt(file_content, job_description if job_description.strip() else None, job_role if job_role.strip() else None)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert ATS resume analyst and HR professional. Return ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4000,
        )
        raw = response.choices[0].message.content

        data = parse_ai_json(raw)
        if data:
            render_results(data)
        else:
            st.warning("Could not parse structured output. Raw response:")
            st.markdown(raw)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
