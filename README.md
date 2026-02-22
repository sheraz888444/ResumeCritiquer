# AI Resume Critiquer

AI-powered resume analysis with ATS scoring, skill gap analysis, and improvement suggestions.

## Run locally

```bash
pip install -r requirements.txt
# Set GROQ_API_KEY in .env (get free key at https://console.groq.com)
streamlit run main.py
```

## Deploy on Railway

1. Push this repo to GitHub.
2. In [Railway](https://railway.app), **New Project** → **Deploy from GitHub** → select the repo.
3. Add a **Variable**: `GROQ_API_KEY` = your Groq API key.
4. Railway will use the **Procfile** to run:
   ```
   web: streamlit run main.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```
5. Generate a **domain** in the project Settings to get a public URL.

No Dockerfile needed; Railway uses Nixpacks with the Procfile and `requirements.txt`.
