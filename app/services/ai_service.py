import json
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from app.utils.exam_data import exams, units, exam_fields
from app.services.pdf_service import processar_exames, extract_text_from_pdf
from collections import defaultdict

load_dotenv(find_dotenv('app/config/.env'))


def criar_client_openai():
    """
    Inicializa e retorna um cliente OpenAI para comunicação com a API DeepSeek.

    :return: Instância do cliente OpenAI.
    """
    load_dotenv(find_dotenv('.env'))

    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )


def contract_loader():
    """
    Lê um arquivo JSON e retorna seu conteúdo como um dicionário Python.
    """
    # Caminho relativo ao script que está sendo executado
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "contrato.json")

    # Normaliza o caminho para garantir compatibilidade com diferentes SOs
    json_path = os.path.normpath(json_path)

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def gerar_system_prompt(text, json):
    """
    Retorna o prompt do sistema utilizado para extração de exames de um texto.

    :return: String com o prompt do sistema.
    """
    prompts = []
    exames = processar_exames(json, exam_fields, exams, units)
    for page in text:
        contrato = contract_loader()
        prompt = f"""
                You are an AI specialized in extracting exam data from PDF text. Your task is to read the provided text 
                and generate a structured JSON object that includes only the exams listed in the units dictionary below.

                ### Understanding the Data Structure:

                - exams: List with the exams in the pdf
                - categories: List with the categories of the exams (e.g., "Eritrograma" and "Leucograma" in a blood test).
                - fields: List with the fields in the categories.(e.g., "Eritrocitos" inside "Eritograma" )

                You need to group the exams inside the lists.


                Rules for Data Extraction:
                1. Units Dictionary Requirement:
                   - If the units dictionary is empty, do not process the text or generate any output.
                2. Exam Filtering:
                   - Only include exams whose "nome_principal" exists in the units dictionary. Ignore all other exams.
                3. Unit Standardization:
                   - Ensure that unit measures strictly follow the "unidade" field from the units dictionary. 
                   Convert them if necessary.
                4. Exam ID Assignment:
                   - Use the "id" from the units dictionary as the unique identifier for each exam.
                5. Exam name:
                    - If one of the exam names is present within "variacoes" in the unit dictionary, 
                convert it to the name found in "nome_principal." Example: Cobalamina to Vitamin B12.
                6. Missing Exams:
                    - If a field is present in the unit dictionary but does not exist in the text, you can ignore it.
                7. Data Structure:
                   - The JSON must contain a "date" field for the exam date.
                   - Exams must be stored in the "exams" array.
                   - Each exam must contain:
                     - "id": The corresponding ID from the units dictionary.
                     - "method": The method used to perform the exam.
                     - "categories": An array of categories, with optional subcategories.
                     - "fields": The list of extracted exam fields.
                     - "values": The extracted exam values with their unit, type, and reference ranges.
                8. Missing Data:
                   - If a required field is missing in the input, leave it empty ("") or null.
                9. Output Restriction:
                   - The response must contain only the JSON object—no additional text, explanations, or comments.

                units:
                {exames}

                EXAMPLE JSON OUTPUT:
                {contrato}
                """

        prompts.append(prompt)

    return prompts


def process_text_with_ai(text, json_data):
    prompts = gerar_system_prompt(text, json_data)
    responses = []
    client = criar_client_openai()

    for prompt, page in zip(prompts, text):

        user_prompt = f"{page}"

        messages = [{"role": "system", "content": prompt},
                    {"role": "user", "content": user_prompt}]

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={'type': 'json_object'}
        )

        responses.append(response)

    # Criando um dicionário para agrupar exames por ID único
    merged_data = defaultdict(lambda: {'exams': []})

    for obj in responses:
        obj = json.loads(obj.choices[0].message.content)  # Converte para JSON válido
        key = obj.get('date')  # Usa .get() para evitar erro se 'date' não existir
        if not key:
            continue  # Pula se não houver data

        if key not in merged_data:
            merged_data[key] = {k: v for k, v in obj.items()}
            merged_data[key]['exams'] = []  # Garante que exams existe

        if 'exams' in obj:
            merged_data[key]['exams'].extend(obj['exams'])

    # Convertendo de volta para lista
    result = list(merged_data.values())

    # Retorna o JSON formatado como string
    return json.dumps(result)

