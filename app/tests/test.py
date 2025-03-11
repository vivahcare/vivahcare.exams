from ollama import chat
from pydantic import Field

from app.utils.contract_loader import carregar_contrato
from app.services.pdf_service import extrair_texto_pdf, identificar_exames_com_unidades
from app.utils import exam_data

from pydantic import BaseModel
from typing import List, Optional, Union


class Reference(BaseModel):
    min: Optional[Union[int, float]] = Field(..., example=4)
    max: Optional[Union[int, float]] = Field(..., example=5)
    value: str = Field(..., example="nao reagente")
    ref_group: str = Field(..., example="male")

class Value(BaseModel):
    value: str = Field(..., example="2")
    unit_measure: str = Field(..., example="milhoes/mm")
    value_type: str = Field(..., example="string")
    reference: Reference

class FieldModel(BaseModel):
    field: str = Field(..., example="HEMÁCIAS")
    label: str = Field(..., example="HEMÁCIAS")
    values: List[Value]
    type: str = Field(..., example="input")
    index: int = Field(..., example=0)

class Category(BaseModel):
    category_name: str = Field(..., example="ERITROGRAMA")
    fields: List[FieldModel]

class ExamDetails(BaseModel):
    type: str = Field(..., example="HEMOGRAMA COMPLETO")
    method: str = Field(..., example="luminescence")
    category: List[Category]

class Exam(BaseModel):
    id: str = Field(..., example="id unico da consulta")
    exam_link: str = Field(..., example="https://example.com/exam/abcde")
    date: str = Field(..., example="2014-03-24")
    gender: int = Field(..., example=0)
    version: int = Field(..., example=1)
    age: int = Field(..., example=30)
    exams: List[ExamDetails]


text = extrair_texto_pdf('../Mais exames/Exame de FERNANDO AKIRA HIRAMATSU - janeiro 2018.pdf')

def gerar_system_prompt():
    """
    Retorna o prompt do sistema utilizado para extração de exames de um texto.

    :return: String com o prompt do sistema.
    """
    prompts = []
    for page in text:
        exames = identificar_exames_com_unidades(page, exams.exames, exams.unidades)
        contrato = carregar_contrato('data/contrato.json')
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

def gerar_output():
    prompts = gerar_system_prompt()
    responses = []

    for prompt, page in zip(prompts, text):
        print(prompt)
        user_prompt = f"{page}"

        messages = [{"role": "system", "content": prompt},
                    {"role": "user", "content": user_prompt}]

        response = chat(
            messages= messages,
            model='deepseek-r1:8b',
            format=Exam.model_json_schema(),
        )

        expected_output = Exam.model_validate_json(response.message.content)

        print(expected_output)


        # response = client.chat.completions.create(
        #     model="deepseek-chat",
        #     messages=messages,
        #     stream=True,
        #     response_format={'type': 'json_object'}
        # )
        responses.append(expected_output)

    return responses



print(gerar_output())

# response = chat(
#   messages=[
#     {
#         'role': 'system',
#         'content': gerar_system_prompt()[0],
#     },
#     {
#       'role': 'user',
#       'content': text[0],
#     }
#   ],
#   model='deepseek-r1:8b',
#   format=Exam.model_json_schema(),
# )

