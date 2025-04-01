from app.services.ai_service import process_text_with_ai, gerar_system_prompt
from app.services.pdf_service import extract_text_from_pdf
from app.services.s3_service import get_pdf_from_s3, list_s3_files

json_data = {
    "storage_path": "exams/EXAME DE SANGUE MAXWELL.pdf",
    "exams": [
        {
            "id": "f8912821-670f-4cb5-813a-5ad76bbe7e45",
            "type": "Hemograma completo"
        },
        {
            "id": "f8912821-670f-4cb5-813a-5ad76bbe7e46",
            "type": "ureia"
        },
        {
            "id": "f8912821-670f-4cb5-813a-5ad76bbe7e47",
            "type": "sodio"
        }

    ]
}

folder = json_data["storage_path"]

# folder = '2020-08 - Exame de sangue completo.pdf'
list_s3_files()


pdf_path = get_pdf_from_s3(json_data, f"exams/{folder}")

# 2. Extrair texto do PDF
extracted_text = extract_text_from_pdf(f'{pdf_path}')

exames = gerar_system_prompt(extracted_text, json_data)

# 3. Processar o texto com IA (usando o JSON fornecido)
ai_response = process_text_with_ai(extracted_text, json_data, indent=2)