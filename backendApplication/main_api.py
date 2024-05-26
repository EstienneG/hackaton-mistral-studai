from fastapi import FastAPI
from pydantic import BaseModel
import langchain_core
import json

# Importer votre fonction de traitement du texte
from generatesummaryfromdocuments import generate_summary_from_document

app = FastAPI()

class ChapterSummaryRequest(BaseModel):
    chapter_selected: str
    difficulty_selected: str


class ChapterSummaryResponse(BaseModel):
    chapter_summary: str

@app.post("/generate-summary", response_model=ChapterSummaryResponse)
def process_text_endpoint(request: ChapterSummaryRequest):
    output_text = generate_summary_from_document(request.chapter_selected, request.difficulty_selected)

    return {"chapter_summary":output_text}

@app.post("/generate-exercise", response_model=ChapterSummaryResponse)
def process_text_endpoint(request: ChapterSummaryRequest):
    output_text = generate_summary_from_document(request.chapter_selected, request.difficulty_selected)

    return {"chapter_summary":output_text}
