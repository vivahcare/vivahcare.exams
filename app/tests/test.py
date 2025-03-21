from app.services.ai_service import process_text_with_ai
from app.services.pdf_service import extract_text_from_pdf
from app.services.s3_service import get_pdf_from_s3


json_data = {
    "storage_path": "5e1cad38-79a6-48a4-804b-7cc2de99364a/exmae123.pdf",
    "exams": [
        {
            "id": "f8912821-670f-4cb5-813a-5ad76bbe7e45",
            "type": "Hemograma completo"
        },

    ]
}

folder = json_data["storage_path"]


pdf_path = get_pdf_from_s3(json_data, f"exams/{folder}")

# 2. Extrair texto do PDF
extracted_text = extract_text_from_pdf(f'{pdf_path}')

# 3. Processar o texto com IA (usando o JSON fornecido)
ai_response = process_text_with_ai(extracted_text, json_data)

print(ai_response)