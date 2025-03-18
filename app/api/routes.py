from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.s3_service import get_pdf_from_s3
from app.services.ai_service import process_text_with_ai
from app.services.pdf_service import extract_text_from_pdf
from app.config.config import Settings

app = FastAPI()


class ExamRequest(BaseModel):
    json_data: dict


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
def read_root():
    return {"message": "VivahCare API is running!"}


@app.post("/exams")
def get_exam_data(request: ExamRequest):
    """
    Rota que recebe o nome do arquivo PDF, busca no S3, extrai o texto e processa com IA.
    """
    jsondata = request.json_data
    folder = jsondata["storage_path"]
    print(folder)
    try:
        # 1. Baixar PDF do S3
        pdf_path = get_pdf_from_s3(request.json_data, f"exams/{folder}")

        # 2. Extrair texto do PDF
        extracted_text = extract_text_from_pdf(f'{pdf_path}')

        # 3. Processar o texto com IA (usando o JSON fornecido)
        ai_response = process_text_with_ai(extracted_text, request.json_data)

        return {"file_name": folder, "processed_data": ai_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))