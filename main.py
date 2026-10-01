from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os

load_dotenv()
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

# Import EduGenie modules
from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

# Initialize FastAPI
app = FastAPI(title="EduGenie")

# Static files and templates
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Request models
class TopicRequest(BaseModel):
    topic: str

class TextRequest(BaseModel):
    text: str


# Home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


# Q&A
@app.get("/qa")
def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# Explanation
@app.post("/explain/")
def explain_api(data: TopicRequest):
    if not data.topic.strip():
        return {"error": "Please provide a topic."}

    explanation = explain_topic(data.topic)
    return {"topic": data.topic, "explanation": explanation}


# Summarization
@app.post("/summarize/")
def summarize_api(data: TextRequest):
    if not data.text.strip():
        return {"error": "Please provide text to summarize."}

    summary = summarize_text(data.text)
    return {"summary": summary}


# Quiz Generation
@app.post("/quiz/")
def quiz_api(data: TextRequest):
    if not data.text.strip():
        return {"error": "Please provide text for quiz."}

    quiz = generate_quiz(data.text)
    return {"quiz": quiz}


# Learning Recommendations
@app.get("/learn/recommendations")
def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {
        "topic": topic,
        "recommendation": recommendation
    }