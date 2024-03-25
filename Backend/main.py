from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import io
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.process import lmm_response_pdf
from utils.helper import process_uploaded_file

# Load environment variables from .env file (if any)
load_dotenv()

class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Any

app = FastAPI()


@app.post("/predict")
async def predict(request: Request):
    form = await request.form()
    file = form.get("file", None)
    question = form.get("question", None)

    if file is None or question is None:
        return JSONResponse({"error": "File or question data not provided"}, status_code=400)

    try:
        file_content, file_extension = await process_uploaded_file(file)
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    

    if file_extension == "pdf":
        response = lmm_response_pdf(file_content, question)



    # Process the question and file content
    print({"file_name": file.filename, "file_extension": file_extension, "response": response})
    # For now, let's just return the received data
    return JSONResponse({"file_name": file.filename, "file_extension": file_extension, "question": question})