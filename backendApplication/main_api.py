from fastapi import FastAPI
from pydantic import BaseModel
import langchain_core
import json
from retrieval import retrieval
from generate_fill_gap import generate_fill_gap
import yaml

# Importer votre fonction de traitement du texte
from generatesummaryfromdocuments import generate_summary_from_document

app = FastAPI()

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

api_key = config["api_keys"]["mistral_api_key"]
llm_model = config["models"]["llm_model_name"]
embedding_model = config["models"]["embedding_model_name"]

class ChapterSummaryRequest(BaseModel):
    chapter_name: str
    difficulty_selected: str


class ChapterSummaryResponse(BaseModel):
    chapter_summary: str

class ChapterExerciseResponse(BaseModel):
    chapter_exercise: str

@app.post("/generate-summary", response_model=ChapterSummaryResponse)
def process_text_endpoint(request: ChapterSummaryRequest):

    retrieve_cunks_str = retrieval("../data/chromadb", api_key, request.chapter_name)

    # TODO: changer le prompt système du writer dans generate_summary_from_document
    output_text = generate_summary_from_document(retrieve_cunks_str, request.difficulty_selected)

    return {"chapter_summary":output_text}

@app.post("/generate-exercise", response_model=ChapterExerciseResponse)
def process_text_endpoint(request: ChapterSummaryRequest):
    retrieved_cunks_str = retrieval("../data/chromadb", api_key, request.chapter_name)

    exercise = generate_fill_gap(retrieved_cunks_str, request.difficulty_selected)

    return {"chapter_exercise": exercise}
