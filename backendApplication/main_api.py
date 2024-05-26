from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import yaml
import os
import tempfile
from pathlib import Path
import logging
from generatesummaryfromdocuments import generate_summary_from_document
from retrieval import retrieval
from generate_exercise import generate_fill_gap, generate_qcm
from vector_db import upload_document
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

api_key = config["api_keys"]["mistral_api_key"]
llm_model = config["models"]["llm_model_name"]
embedding_model = config["models"]["embedding_model_name"]

class ChapterSummaryRequest(BaseModel):
    chapter_name: str
    difficulty_selected: str
    db_workspace_name: str

class ChapterSummaryResponse(BaseModel):
    chapter_summary: str

class UploadDocumentResponse(BaseModel):
    chapters: list 

class ChapterExerciseResponse(BaseModel):
    chapter_exercise: str

@app.post("/generate-summary", response_model=ChapterSummaryResponse)
def generate_summary_endpoint(request: ChapterSummaryRequest):
    retrieved_chunks_str = retrieval(f"../data/{request.db_workspace_name}/chromadb", api_key, request.chapter_name)
    
    output_text = generate_summary_from_document(retrieved_chunks_str, request.difficulty_selected)

    return {"chapter_summary": output_text}

@app.post("/generate-exercise", response_model=ChapterExerciseResponse)
def generate_exercise_endpoint(request: ChapterSummaryRequest):
    retrieved_chunks_str = retrieval(f"../data/{request.db_workspace_name}/chromadb", api_key, request.chapter_name)
    
    exercise = generate_fill_gap(retrieved_chunks_str, request.difficulty_selected)

    return {"chapter_exercise": exercise}

@app.post("/generate-qcm", response_model=ChapterExerciseResponse)
def generate_exercise_endpoint(request: ChapterSummaryRequest):
    retrieved_chunks_str = retrieval(f"../data/{request.db_workspace_name}/chromadb", api_key, request.chapter_name)
    
    exercise = generate_qcm(retrieved_chunks_str, request.difficulty_selected)

    return {"chapter_exercise": exercise}

@app.post("/upload_document", response_model=UploadDocumentResponse)
async def upload_document_endpoint(upload_file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = upload_file.filename
            workspace_name = Path(file_name).stem

            file_path = os.path.join(temp_dir, file_name)

            # Save the uploaded file
            with open(file_path, "wb") as buffer:
                buffer.write(await upload_file.read())

            # Process the document
            chapters_structure = upload_document(file_path, api_key=api_key, output_path="", embedding_model_name=embedding_model, workspace_name=workspace_name)

            # Return the response
            response = UploadDocumentResponse(chapters=chapters_structure)
            return JSONResponse(content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Failed to process document: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
