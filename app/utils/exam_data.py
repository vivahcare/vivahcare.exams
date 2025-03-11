import unidecode

# Dicionário unificado "exames" contendo informações de exames, variações e agrupados por categoria

exams = {
    # ========================
    # Hemograma - Série Vermelha / Eritrograma
    # ========================
    "Hemácias": ["Eritrócitos totais", "Eritrócitos", "Glóbulos vermelhos"],
    "Hemoglobina": ["Hb"],
    "Hematócrito": ["Ht", "Hct"],
    "V.C.M": ["VGM", "Volume Corpuscular Médio", "Volume Globular Médio"],
    "H.C.M": ["HGM", "Hemoglobina Corpuscular Média", "Hemoglobina Globular Média"],
    "C.H.C.M": ["Concentração HCM", "Concentração de Hemoglobina Corpuscular Média"],
    "RDW": ["Amplitude de Distribuição dos Glóbulos Vermelhos"],

    # ========================
    # Hemograma - Série Branca / Leucograma
    # ========================
    "Leucócitos": ["Glóbulos brancos", "Leucócitos totais"],
    "Neutrófilos": [],
    "Segmentados": ["Neutrófilos segmentados"],
    "Bastonetes": ["Neutrófilos bastonetes"],
    "Eosinófilos": ["granulócitos eosinófilos", "acidófilos"],
    "Basófilos": ["granulócitos basófilos"],
    "blastos": [],
    "monócitos": [],
    "linfócitos atípicos": ["linfócitos reativos"],
    "linfócitos típicos": ["linfócitos"],
    "promielócitos": [],
    "mielócitos": [],
    "metamielócitos": [],

    # ========================
    # Hemograma - Série Plaquetária / Plaquetas
    # ========================
    "Plaquetas": ["trombócitos"],
    "MPV": ["volume plaquetário médio"],
    "Plaquetas Óticas Contagem": [],

    # ========================
    # Vitaminas
    # ========================
    "Vitamina B12": ["Cobalamina"],
    "Vitamina D": ["Calciferol", "hidroxivitaminaD", "vitamina D - 25 hidroxi", "25-hidroxivitaminaD", "vit D3 + D2", "25 OHD"],
    "Vitamina A": ["Retinol"],
    "Vitamina C": ["Ácido ascórbico"],
    "Vitamina H-B7-B8": ["Biotina", "Vitamina B8"],
    "Vitamina B1": ["Tiamina"],
    "Vitamina B2": ["FAD", "Pelagra", "Riboflavina"],
    "Vitamina B3": ["Nicotinamida", "Niacina", "Vit. PP"],
    "Vitamina B5": ["Ácido pantotênico", "Pantatotenato"],
    "Vitamina B6": ["Piridoxina"],
    "Vitamina E": ["Tocoferol"],
    "Vitamina k": ["filoquinona", "fitonadiona", "hepatopatias"],
    "Vitamina B9": ["ácido fólico"],

    # ========================
    # Minerais
    # ========================
    "Sódio": ["natremia", "Na+ no sangue"],
    "zinco": ["zinco no soro", "Zn no soro", "zincemia"],
    "ferritina": [],
    "ferro": ["ferro livre", "ferro circulante", "ferro total"],
    "magnésio": ["magnesemia", "Mg"],
    "cálcio": ["calcemia"],
    "potássio": ["kalemia", "ionograma", "potassemia"],
    "fósforo": ["fosfato"],

    # ========================
    # Teste Hormonal
    # ========================
    "Folículo": ["FSH"],
    "Luteinizante": ["LH"],
    "Insulina": ["insulina circulante", "insulina basal"],
    "Prolactina": ["PRL"],
    "Testosterona livre": ["testo livre calculada", "androgenio livre"],
    "testosterona total": ["testosterona"],
    "hormonio paratireoidiano": ["PTH", "Paratormônio", "hormonio da paratireóide"],
    "antígeno prostático específico": ["PSA"],
    "dehidroepiandrosterona": ["DHEA", "androstenolona"],
    "hormonio do crescimento": ["GH", "HGH", "hormônio somatotrófico", "somatotrofina"],
    "cortisol": ["hidrocortisona"],
    "estrona": ["E1"],
    "estradiol": ["E2", "17 Beta estradiol"],
    "estriol": ["E3", "estrógenos em gestante"],
    "progesterona": ["PRG"],
    "Tiroestimulante": ["TSH"],
    "Triiodotironina": ["T3", "TT3"],
    "Tiroxina": ["T4", "Tetraiodotironina"]
}

unidades_hemograma = {
    # Série Vermelha / Eritrograma
    "Hemácias": "milhões/mm³",
    "Hemoglobina": "g/dL",
    "Hematócrito": "%",
    "V.C.M": "fL",
    "H.C.M": "pg",
    "C.H.C.M": "g/dL",
    "RDW": "%",

    # Série Branca / Leucograma
    "Leucócitos": "/mm³",
    "Neutrófilos": "/mm³",
    "Segmentados": "/mm³",
    "Bastonetes": "/mm³",
    "Eosinófilos": "/mm³",
    "Basófilos": "/mm³",
    "blastos": "/mm³",
    "monócitos": "/mm³",
    "linfócitos atípicos": "/mm³",
    "linfócitos típicos": "/mm³",
    "promielócitos": "/mm³",
    "mielócitos": "/mm³",
    "metamielócitos": "/mm³",

    # Série Plaquetária / Plaquetas
    "Plaquetas": "/mm³",
    "MPV": "fL",
    "Plaquetas Óticas Contagem": "/mm³"
}

unidades_vitaminas_minerais = {
    # ========================
    # Vitaminas
    # ========================
    "Vitamina B12": "pg/mL",
    "Vitamina D": "ng/mL",
    "Vitamina A": "mg/L",
    "Vitamina C": "mg/L",
    "Vitamina H-B7-B8": "mg/L",
    "Vitamina B1": "mg/L",
    "Vitamina B2": "mg/L",
    "Vitamina B3": "mg/L",
    "Vitamina B5": "mg/L",
    "Vitamina B6": "mg/L",
    "Vitamina E": "mg/L",
    "Vitamina k": "mg/L",
    "Vitamina B9": "mg/L",

    # ========================
    # Minerais
    # ========================
    "Sódio": "mmol/L",
    "Zinco": "mg/L",
    "Ferritina": "ng/mL",
    "Ferro": "µg/dL",
    "Magnésio": "mg/dL",
    "Cálcio": "mg/dL",
    "Potássio": "mmol/L",
    "Fósforo": "mg/dL"
}

unidades_teste_hormonal = {
    # =================================
    # Teste Hormonal
    # =================================

    # FSH (Folículo Estimulante)
    "Folículo": "mUI/mL",

    # LH (Luteinizante)
    "Luteinizante": "mUI/mL",

    # Insulina
    "Insulina": "µUI/mL",

    # Prolactina
    "Prolactina": "ng/mL",

    # Testosterona livre
    "Testosterona livre": "pg/mL",

    # Testosterona total
    "testosterona total": "ng/dL",

    # Hormônio Paratireoidiano (PTH)
    "hormonio paratireoidiano": "pg/mL",

    # Antígeno Prostático Específico (PSA)
    "antígeno prostático específico": "ng/mL",

    # Dehidroepiandrosterona (DHEA)
    "dehidroepiandrosterona": "µg/dL",

    # Hormônio do Crescimento (GH)
    "hormonio do crescimento": "ng/mL",

    # Cortisol
    "cortisol": "µg/dL",

    # Estrona (E1)
    "estrona": "pg/mL",

    # Estradiol (E2)
    "estradiol": "pg/mL",

    # Estriol (E3)
    "estriol": "ng/mL",

    # Progesterona
    "progesterona": "ng/mL",

    # Tiroestimulante (TSH)
    "Tiroestimulante": "µUI/mL",

    # Triiodotironina (T3)
    "Triiodotironina": "ng/dL",

    # Tiroxina (T4)
    "Tiroxina": "µg/dL"
}

unidades_fezes_urina = {
    "Volume": "mL",
    "Densidade": "g/L",
}

unidades_exames_gerais = {
    # =================================
    # Perfil Lipídico
    # =================================
    "Colesterol Total": "mg/dL",
    "Colesterol HDL": "mg/dL",
    "Colesterol LDL": "mg/dL",
    "Colesterol VLDL": "mg/dL",
    "Triglicerídeos": "mg/dL",

    # =================================
    # Metabolismo e Outros
    # =================================
    "Glicose": "mg/dL",
    "Creatinina": "mg/dL",
    "Ureia": "mg/dL",
    "Ácido Úrico": "mg/dL",
    "Cálcio Ionizado": "mg/dL",
    "Hemoglobina Glicada (HbA1c)": "%",

    # =================================
    # Enzimas / Marcadores
    # =================================
    "TGO": "U/L",  # AST
    "TGP": "U/L",  # ALT
    "Gama GT": "U/L",
    "Fosfatase Alcalina": "U/L",
    "Amilase": "U/L",
    "Lipase": "U/L",

    # =================================
    # Inflamação e Autoimunes
    # =================================
    "Proteína C Reativa (PCR)": "mg/L",
    "PCR Ultra-Sensível": "mg/L",
    "Fator Reumatoide": "UI/mL",
    "Velocidade de Hemossedimentação": "mm/h",

    # =================================
    # Outros
    # =================================
    "Beta-hCG": "mUI/mL"
}

units = {
    "hemograma": unidades_hemograma,
    "vitaminas_minerais": unidades_vitaminas_minerais,
    "teste_hormonal": unidades_teste_hormonal,
    "fezes_urina": unidades_fezes_urina,
    "exames_gerais": unidades_exames_gerais
}


def padronizar_exames(exams_dict):
    padronizado = {}
    for exame, variacoes in exams_dict.items():
        exame_padronizado = unidecode.unidecode(exame.lower())
        variacoes_padronizadas = [unidecode.unidecode(v.lower()) for v in variacoes]
        padronizado[exame_padronizado] = variacoes_padronizadas
    return padronizado

