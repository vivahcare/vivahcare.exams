import re
import unicodedata
import unidecode
from PyPDF2 import PdfReader
from app.utils.exam_data import units, exams, padronizar_exames


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


def identificar_exames_com_unidades(texto, exames_dict, unidades_nested, exams_json):
    """
    Adiciona a verificação se o exame está presente em exams_json antes de procurar no texto.
    Retorna erro se um exame presente em exams_json não for encontrado no texto.
    """

    def busca_unidade(unidades_nested, exame):
        for grupo in unidades_nested.values():
            grupo_normalizado = {remover_acentos(k.lower()): v for k, v in grupo.items()}
            if exame in grupo_normalizado:
                return grupo_normalizado[exame]
        return ""

    # Normaliza todas as entradas
    texto_normalizado = remover_acentos(texto.lower())

    exames_dict = {remover_acentos(k.lower()): [remover_acentos(v.lower()) for v in vals] for k, vals in
                   exames_dict.items()}
    unidades_nested = {remover_acentos(k.lower()): {remover_acentos(sub_k.lower()): sub_v for sub_k, sub_v in v.items()}
                       for k, v in unidades_nested.items()}
    exams_json = {"storage_path": exams_json["storage_path"],
                  "exams": [{"id": e["id"], "type": remover_acentos(e["type"].lower())} for e in exams_json["exams"]]}

    exames_permitidos = {e["type"]: e["id"] for e in exams_json["exams"]}
    resultados = []
    exames_nao_encontrados = []

    for exame, variacoes in exames_dict.items():
        if exame not in exames_permitidos:
            continue  # Ignora exames que não estão na lista

        # Procura o nome original no texto
        padrao_original = r'\b' + re.escape(exame) + r'\b'
        encontrado_original = re.search(padrao_original, texto_normalizado, re.IGNORECASE)

        found_variation = ""
        if not encontrado_original:
            for var in variacoes:
                padrao_var = r'\b' + re.escape(var) + r'\b'
                if re.search(padrao_var, texto_normalizado, re.IGNORECASE):
                    found_variation = var
                    break

        if encontrado_original or found_variation:
            unidade = busca_unidade(unidades_nested, exame)
            entry = {
                "id": exames_permitidos[exame],
                "nome_original": exame,
                "variação": "" if encontrado_original else found_variation,
                "unidade": unidade
            }
            resultados.append(entry)
        else:
            exames_nao_encontrados.append(exame)

    # if exames_nao_encontrados:
    #     raise ValueError(
    #         f"Os seguintes exames estavam no JSON, mas não foram encontrados no texto: {', '.join(exames_nao_encontrados)}")

    return resultados


# def identificar_exames_com_unidades(texto, exames_dict, unidades_nested):
#     """
#     Recebe:
#       - texto: string a ser analisada.
#       - exames_dict: dicionário onde cada chave é o nome oficial do exame e o valor é uma lista de variações.
#       - unidades_nested: dicionário aninhado com os grupos de unidades, onde em cada subdicionário
#         a chave é o nome oficial do exame e o valor é a unidade.
#
#     Para cada exame, procura no texto tanto o nome original quanto as variações.
#       - Se o nome original for encontrado, o campo "variação" ficará em branco.
#       - Se não, mas uma variação for encontrada, esse valor é registrado.
#
#     A função utiliza busca_unidade() para procurar a unidade correspondente.
#
#     Retorna uma lista de dicionários com a estrutura:
#       {
#          "nome_original": <nome oficial>,
#          "variação": <variação encontrada ou vazio>,
#          "unidade": <unidade ou vazio se não encontrada>
#       }
#     """
#
#     def busca_unidade(unidades_nested, exame):
#         """
#         Percorre todos os subdicionários do dicionário aninhado unidades_nested para
#         encontrar a unidade associada ao exame. Se não encontrar, retorna uma string vazia.
#         """
#         for grupo in unidades_nested.values():
#             if exame in grupo:
#                 return grupo[exame]
#         return ""
#
#     resultados = []
#
#     for exame, variacoes in exames_dict.items():
#         # Procura o nome original no texto (case-insensitive)
#         padrao_original = r'\b' + re.escape(exame) + r'\b'
#         encontrado_original = re.search(padrao_original, texto, re.IGNORECASE)
#
#
#         found_variation = ""
#         # Se o nome original não for encontrado, procura por cada variação
#         if not encontrado_original:
#             for var in variacoes:
#                 # Converte a variação para maiúsculo para a busca
#                 var_upper = var.upper()
#                 padrao_var = r'\b' + re.escape(var_upper) + r'\b'
#                 # Busca diretamente a variação em maiúsculas no texto
#                 if re.search(padrao_var, texto):
#                     found_variation = var
#                     break
#
#         # Se encontrou o nome original ou uma variação, registra o exame
#         if encontrado_original or found_variation:
#             # Aqui, usamos a função busca_unidade para procurar a unidade no dicionário aninhado
#             unidade = busca_unidade(unidades_nested, exame)
#             entry = {
#                 "nome_original": exame,
#                 "variação": "" if encontrado_original else found_variation,
#                 "unidade": unidade
#             }
#             resultados.append(entry)
#
#         if len(resultados) == 0:
#             resultados.append('Sem unidades')
#
#     return resultados

exams_json = {
    "storage_path": "exams/123/456.pdf",
    "exams": [
        {"id": "09c23a20-8303-4f99-b085-baa65bb28400", "type": "hemacias"},
        {"id": "cdf50e29-773e-4006-a850-d2f3702d4104", "type": "leucocitos"},
        {"id": "cdf50e29-773e-4006-a850-d2f3702d4106", "type": "v.c.m"}
    ]
}

text = extract_text_from_pdf('downloads/exams/2.pdf')

exames = identificar_exames_com_unidades(text[0], exams, units, exams_json)
