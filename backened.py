from fastapi import FastAPI
from pydantic import BaseModel
from youtube_project import main

app = FastAPI()

class QuestionRequest(BaseModel):
    video_id: str
    query: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    answer = main(request.video_id, request.query)
    return {"video_id": request.video_id,"question": request.query,"answer": answer}