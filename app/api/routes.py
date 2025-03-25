import json
from functools import lru_cache
import asyncio

import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
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
async def get_exam_data(request: ExamRequest, background_tasks: BackgroundTasks):
    """
    Rota que recebe o nome do arquivo PDF, envia confirmação imediata
    e processa em segundo plano.
    """
    # Enviar resposta de recebido imediatamente
    received_response = {
        "status": "received",
        "message": "Solicitação de exame recebida com sucesso",
        "file_name": request.json_data.get("storage_path", "unknown")
    }

    # Adicionar tarefa em segundo plano para processamento
    background_tasks.add_task(process_exam, request)

    return received_response


async def process_exam(request: ExamRequest):
    """
    Função para processamento assíncrono do exame em segundo plano
    """
    jsondata = request.json_data
    url = "https://api.vivahcare.com/exams/update"
    folder = jsondata["storage_path"]

    try:
        # 1. Baixar PDF do S3
        pdf_path = get_pdf_from_s3(request.json_data, f"exams/{folder}")

        # 2. Extrair texto do PDF
        extracted_text = extract_text_from_pdf(f'{pdf_path}')

        # 3. Processar o texto com IA (usando o JSON fornecido)
        ai_response = process_text_with_ai(extracted_text, request.json_data)

        try:
            # Tentar parsear a resposta
            parsed_response = json.loads(ai_response)

            # Verificar se é uma lista e pegar o primeiro item
            if isinstance(parsed_response, list) and parsed_response:
                json_data = parsed_response[0]
            else:
                # Se não for uma lista válida, criar um JSON mínimo
                json_data = {"error": "Invalid response format"}

            # Enviar requisição PUT
            response = requests.put(url, json=json_data)

            # Imprimir o código de status
            print("Status Code:", response.status_code)

            # Imprimir o texto da resposta
            print("Response Text:", response.text)

            # Imprimir os cabeçalhos da resposta
            print("Response Headers:", response.headers)

            # Se for uma resposta JSON, pode tentar imprimir o JSON
            try:
                print("Response JSON:", response.json())
            except ValueError:
                print("Resposta não é um JSON válido")

            # Verificar resposta
            if response.status_code not in [200, 201]:
                print(f"Erro na atualização: {response.status_code} - {response.text}")

        except json.JSONDecodeError:
            # Se o parse falhar, criar um JSON mínimo
            json_data = {"error": "Invalid JSON response"}
            print("Falha ao decodificar JSON")

    except Exception as e:
        # Logging de erro para falhas no processamento
        print(f"Erro no processamento do exame: {e}")


# @app.post("/exams")
# def get_exam_data(request: ExamRequest):
#     """
#     Rota que recebe o nome do arquivo PDF, busca no S3, extrai o texto e processa com IA.
#     """
#     jsondata = request.json_data
#     url = "https://api.vivahcare.com/exams/update"
#     folder = jsondata["storage_path"]
#     try:
#         # 1. Baixar PDF do S3
#         pdf_path = get_pdf_from_s3(request.json_data, f"exams/{folder}")
#
#         # 2. Extrair texto do PDF
#         extracted_text = extract_text_from_pdf(f'{pdf_path}')
#
#         # 3. Processar o texto com IA (usando o JSON fornecido)
#         ai_response = process_text_with_ai(extracted_text, request.json_data)
#
#         try:
#             json_data = json.dumps(request.json_data)
#             response = requests.put(url, data=json_data)
#
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))
#
#         return {"file_name": folder, "processed_data": ai_response}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))