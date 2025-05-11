from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

app = Flask(__name__)
CORS(app, origins=["https://smart-career-coach-frontend.vercel.app"])

# ✅ Resume Generation Route
@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    data = request.get_json()
    name = data.get('name', 'User')
    skills = data.get('skills', 'Python, HTML, CSS')
    experience = data.get('experience', '1 year internship at XYZ')
    job_title = data.get('job_title', 'Software Developer')

    prompt = f"""Write a professional 3-section resume for someone named {name} applying for a {job_title} position. 
Highlight their skills in {skills}, and experience: {experience}."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        resume_text = response.choices[0].message.content.strip()
        return jsonify({"resume": resume_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Job Description Analyzer Route
@app.route('/api/analyze-jd', methods=['POST'])
def analyze_job_description():
    data = request.get_json()
    resume_skills = data.get('skills', '')
    job_description = data.get('job_description', '')

    prompt = f"""
Extract key skills and technologies from this job description:\n\n{job_description}\n\n
Then compare them with the candidate's resume skills: {resume_skills}\n
Return a brief match score out of 100 and list overlapping + missing skills.
Respond in JSON format like this:
{{
  "match_score": 82,
  "overlapping_skills": ["Python", "AWS"],
  "missing_skills": ["Django", "CI/CD"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result_text = response.choices[0].message.content.strip()
        result_json = json.loads(result_text)
        return jsonify(result_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/mock-interview', methods=['POST'])
def mock_interview():
    data = request.get_json()
    job_title = data.get('job_title', 'Software Developer')
    skills = data.get('skills', 'Python, SQL, AWS')

    prompt = f"""
Generate 5 mock technical interview questions for a {job_title} role.
Base them on these skills: {skills}.
Just list the questions only, no answers.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        questions = response.choices[0].message.content.strip()
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/mock-answer', methods=['POST'])
def mock_answer():
    data = request.get_json()
    question = data.get('question', '')

    prompt = f"""Provide a strong, concise answer to the following technical interview question:\n\n{question}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
