import json
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from app.utils.exam_data import exams, units
from app.services.pdf_service import identificar_exames_com_unidades, extract_text_from_pdf
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


def gerar_system_prompt(text):
    """
    Retorna o prompt do sistema utilizado para extração de exames de um texto.

    :return: String com o prompt do sistema.
    """
    prompts = []
    for page in text:
        exames = identificar_exames_com_unidades(page, exams, units)
        contrato = contract_loader()

        prompt = f"""
        You are an AI specialized in extracting exam data from PDF text. Read the provided text and output a valid JSON object
        with keys for exam details. For each exam field, ensure that the unit measures conform to the custom dictionary provided
        below, converting it if necessary. Do not include any additional text; output only the valid JSON object.
        Leave any missing fields empty.
    
        units:
        {exames}
    
        EXAMPLE JSON OUTPUT:
        {contrato}
        """

        prompts.append(prompt)

    return prompts


def process_text_with_ai(text):
    prompts = gerar_system_prompt(text)
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
        key = obj.get('id')  # Usa .get() para evitar erro se 'id' não existir
        if not key:
            continue  # Pula se não houver ID

        if key not in merged_data:
            merged_data[key] = {k: v for k, v in obj.items()}
            merged_data[key]['exams'] = []  # Garante que exams existe

        if 'exams' in obj:
            merged_data[key]['exams'].extend(obj['exams'])

    # Convertendo de volta para lista
    result = list(merged_data.values())

    return result


# text = extract_text_from_pdf('downloads/exams/Hemograma_Completo.pdf')
#
# print(text)
#
# print(process_text_with_ai(text))