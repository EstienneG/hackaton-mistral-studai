from fastapi import FastAPI
from pydantic import BaseModel

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
    output_text = process_text(request.input_text)
    return ChapterSummaryResponse(output_text=output_text)
