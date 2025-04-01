import re
import unicodedata
import unidecode
from PyPDF2 import PdfReader
from fuzzywuzzy import process, fuzz
from app.utils.exam_data import units, exams, padronizar_exames, exam_fields


def get_fields_from_exam(json_data):
    return [exam["type"].lower() for exam in json_data.get("exams", [])]


def extract_text_from_pdf(file_path, page=True):
    """
    Recebe o caminho do arquivo PDF e retorna o texto extraído de todas as páginas em uma lista.

    Parâmetros:
        file_path (str): Caminho completo do arquivo PDF.

    Retorna:
        list: Lista contendo o texto extraído de cada página do PDF.
    """
    texto_por_pagina = ''
    if page:
        reader = PdfReader(file_path)

        texto_por_pagina = [page.extract_text() or "" for page in reader.pages]
    else:
        reader = PdfReader(file_path)
        for page in reader.pages:
            texto_por_pagina += page.extract_text()

    return texto_por_pagina


def encontrar_exames(texto, exames):
    """
    Recebe um texto e um dicionário de exames, onde a chave é o nome oficial do exame
    e o valor é uma lista de variações. Para cada variação, converte-a para maiúsculo e
    utiliza uma busca com correspondência exata de palavra (usando word boundaries) no texto.

    Retorna uma lista com o nome oficial dos exames somente se uma das suas variações (em maiúsculo)
    for encontrada no texto.
    """
    encontrados = []

    for exame, variacoes in exames.items():
        for var in variacoes:
            # Converte a variação para maiúsculo
            var_upper = var.upper()
            # Define um padrão regex para corresponder à palavra completa
            pattern = r'\b' + re.escape(var_upper) + r'\b'
            # Se encontrar a variação no texto, adiciona o exame e passa para o próximo
            if re.search(pattern, texto):
                encontrados.append(exame)
                break

    return encontrados


def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))


def processar_exames(exams_json, exam_fields, exams, units):
    """
    Processa os exames encontrados no exams_json, corrigindo erros de digitação e formatando os resultados.
    """

    # Lista de exames principais (para retornar lista de campos)
    exames_relevantes = ["hemograma completo", "urina", "fezes"]

    # Normaliza os exames do JSON
    exames_no_json = {unidecode.unidecode(e["type"].lower()): e["id"] for e in exams_json["exams"]}

    # Lista de todos os nomes de exames conhecidos (para correção de erros)
    todos_exames_conhecidos = list(exams.keys()) + exames_relevantes

    resultados = []

    for exame_no_json, exame_id in exames_no_json.items():
        # Corrige erro de digitação para qualquer exame
        match, score = process.extractOne(exame_no_json, todos_exames_conhecidos, scorer=fuzz.WRatio)
        exame_final = match if score > 80 else exame_no_json  # Usa o match se for confiável

        if exame_final in exames_relevantes:
            # Busca os campos do exame (se existirem)
            campos_exame = exam_fields.get(exame_final, [])

            campos_formatados = []
            for campo in campos_exame:
                nome_principal = campo
                variacoes = exams.get(campo, [])

                unidade = units.get(campo, "")

                campos_formatados.append({
                    "nome_principal": nome_principal,
                    "variacoes": variacoes,
                    "unidade": unidade
                })

            entry = {
                "id": exame_id,
                "exame": exame_final,
                "campos": campos_formatados
            }
        else:
            # Exames desconhecidos: adiciona nome principal, variações e unidade
            nome_principal = exame_final
            variacoes = exams.get(nome_principal, [])
            unidade = units.get(nome_principal, "")

            entry = {
                "id": exame_id,
                "nome_principal": nome_principal,
                "variacoes": variacoes,
                "unidade": unidade
            }

        resultados.append(entry)

    return resultados

