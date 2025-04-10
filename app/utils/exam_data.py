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
    "Tiroxina": ["T4", "Tetraiodotironina"],

    # ========================
    # Exames de Fezes
    # ========================
    "Parasitológico": ["Exame Parasitológico de Fezes"],
    "Sangue oculto": ["Pesquisa de Sangue Oculto"],
    "Rotavírus": ["Pesquisa de Rotavírus"],
    "Coprocultura/Cultura de Fezes": ["Cultura de Fezes", "Coprocultura"],

    # ========================
    # Exames de Urina
    # ========================
    "Volume": ["Volume Urinário"],
    "Aspecto": ["Aspecto da Urina"],
    "Cor": ["Cor da Urina"],
    "Densidade": ["Densidade Urinária"],
    "pH": ["pH Urinário"],

    # Análise Físico-Química
    "Proteínas": ["Proteinúria"],
    "Glicose urinária": ["Glicosúria"],
    "Corpos Cetônicos": ["Cetonúria"],
    "Hemoglobina urinária": ["Hemoglobinúria"],
    "Bilirrubina": ["Bilirrubinúria"],
    "Urobilinogênio": ["Urobilinogenúria"],
    "Nitrito": ["Teste de Nitrito"],

    # Microscopia do Sedimento
    "Células Epiteliais": ["Células Epiteliais na Urina"],
    "Leucócitos urinária": ["Piúria", "Leucocitúria"],
    "Hemácias urinária": ["Hemoglobinúria", "Hematúria"],
    "Cristais": ["Cristalúria"],
    "Leveduras": ["Leveduras na Urina"],
    "Filamento de Muco": ["Muco Urinário"],
    "Bactérias": ["Bacteriúria"],
    "Cilindros": ["Cilindrúria"],
    "Cetonas": ["Cetonúria"],

    # ========================
    # Exames Gerais
    # ========================
    "HBsAg": ["Antígeno de Superfície da Hepatite B"],
    "Colesterol total": ["Colesterol"],
    "Colesterol HDL": ["High-Density Lipoprotein", "Colesterol bom"],
    "Colesterol LDL": ["Low-Density Lipoprotein", "Colesterol ruim"],
    "Triglicerídeos": ["Triglicerídeos séricos"],
    "Glicose": ["Glicemia", "Glicemia de Jejum"],
    "Hepatite C - Anti HCV": ["Anticorpos contra o vírus da Hepatite C"],
    "Anticorpos Anti-HIV": ["HIV 1 e 2", "Teste de HIV"],
    "Tempo de protrombina (TAP)": ["Tempo de Atividade da Protrombina"],
    "Creatinina": ["Creatina sérica"],
    "Eletroforese de Hemoglobina": ["Frações de Hemoglobina"],
    "Fosfatase Alcalina": ["FA"],
    "Gama GT - Gama Glutamil Transferase": ["GGT", "Gama Glutamil Transpeptidase"],
    "HBs Anti": ["Anticorpos contra Hepatite B"],
    "Homocisteína": ["Homocistinúria"],
    "Bilirrubina Total": ["BT"],
    "Bilirrubina Direta": ["BD"],
    "Bilirrubina Indireta": ["BI"],
    "Tempo de Tromboplastina Parcial Ativado (TTPA)": ["TTPA", "Tempo de tromboplastina ativada"],
    "Desidrogenase Láctica (LDH)": ["Lactato Desidrogenase", "LDH"],
    "Proteína C Reativa (PCR)": ["PCR"],
    "Reticulócitos": ["Contagem de Reticulócitos"],
    "Aspartato Aminotransferase (TGO)": ["TGO", "AST"],
    "Alanina Aminotransferase (TGP)": ["TGP", "ALT"],
    "Transferrina": ["Siderofilina"],
    "VDRL": ["Teste de sífilis", "Reagente para sífilis"],
    "Ureia": ["Nitrogênio Uréico", "BUN"],
    "Velocidade de Hemossedimentação do Sangue (VHS)": ["VHS", "Taxa de Hemossedimentação"],
}

units = {
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
    "Neutrofílos": "/mm³",
    "Segmentados": "/mm³",
    "Bastonetes": "/mm³",
    "Eosinófilos": "/mm³",
    "Basófilos": "/mm³",
    "Blastos": "/mm³",
    "Monócitos": "/mm³",
    "Linfócitos Atípicos": "/mm³",
    "Linfócitos Típicos": "/mm³",
    "Promielócitos": "/mm³",
    "Mielócitos": "/mm³",
    "Metamielócitos": "/mm³",

    # Série Plaquetária / Plaquetas
    "Plaquetas": "/mm³",
    "MPV": "fL",
    "Plaquetas Óticas Contagem": "/mm³",

    # Vitaminas
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
    "Vitamina K": "mg/L",
    "Vitamina B9": "mg/L",

    # Minerais
    "Sódio": "mmol/L",
    "Zinco": "mg/L",
    "Ferritina": "ng/mL",
    "Ferro": "µg/dL",
    "Magnésio": "mg/dL",
    "Cálcio": "mg/dL",
    "Potássio": "mmol/L",
    "Fósforo": "mg/dL",

    # Perfil Lipídico
    "Colesterol Total": "mg/dL",
    "Colesterol HDL": "mg/dL",
    "Colesterol LDL": "mg/dL",
    "Colesterol VLDL": "mg/dL",
    "Triglicerídeos": "mg/dL",

    # Metabolismo e Outros
    "Glicose": "mg/dL",
    "Creatinina": "mg/dL",
    "Ureia": "mg/dL",
    "Ácido Úrico": "mg/dL",
    "Cálcio Ionizado": "mg/dL",
    "Hemoglobina Glicada (HbA1c)": "%",

    # Enzimas / Marcadores
    "TGO": "U/L",  # AST
    "TGP": "U/L",  # ALT
    "Gama GT": "U/L",
    "Fosfatase Alcalina": "U/L",
    "Amilase": "U/L",
    "Lipase": "U/L",

    # Inflamação e Autoimunes
    "Proteína C Reativa (PCR)": "mg/L",
    "PCR Ultra-Sensível": "mg/L",
    "Fator Reumatoide": "UI/mL",
    "Velocidade de Hemossedimentação": "mm/h",

    # Outros
    "Beta-hCG": "mUI/mL",

    # Fezes
    "Volume": "mL",
    "Densidade": "g/L",

    # Teste Hormonal
    "Folículo": "mUI/mL",
    "Luteinizante": "mUI/mL",
    "Insulina": "µUI/mL",
    "Prolactina": "ng/mL",
    "Testosterona Livre": "pg/mL",
    "Testosterona Total": "ng/dL",
    "Hormônio Paratireoidiano": "pg/mL",
    "Antígeno Prostático Específico": "ng/mL",
    "Dehidroepiandrosterona": "µg/dL",
    "Hormônio do Crescimento": "ng/mL",
    "Cortisol": "µg/dL",
    "Estrona": "pg/mL",
    "Estradiol": "pg/mL",
    "Estriol": "ng/mL",
    "Progesterona": "ng/mL",
    "Tiroestimulante": "µUI/mL",
    "Triiodotironina": "ng/dL",
    "Tiroxina": "µg/dL"
}


def padronizar_exames(exams_dict):
    padronizado = {}
    for exame, variacoes in exams_dict.items():
        exame_padronizado = unidecode.unidecode(exame.lower())
        variacoes_padronizadas = [unidecode.unidecode(v.lower()) for v in variacoes]
        padronizado[exame_padronizado] = variacoes_padronizadas
    return padronizado


exam_fields = {
    "hemograma completo": [
        "Hemácias", "Hemoglobina", "Hematócrito", "V.C.M", "H.C.M", "C.H.C.M", "RDW",
        "Leucócitos", "Neutrófilos", "Segmentados", "Bastonetes", "Eosinófilos", "Basófilos",
        "blastos", "monócitos", "linfócitos atípicos", "linfócitos típicos", "promielócitos",
        "mielócitos", "metamielócitos", "Plaquetas", "MPV", "Plaquetas Óticas Contagem"
    ],
    "urina": [
        "Volume", "Aspecto", "Cor", "Densidade", "pH", "Proteínas", "Glicose urinária",
        "Corpos Cetônicos", "Hemoglobina urinária", "Bilirrubina", "Urobilinogênio", "Nitrito",
        "Células Epiteliais", "Leucócitos urinária", "Hemácias urinária", "Cristais", "Leveduras",
        "Filamento de Muco", "Bactérias", "Cilindros", "Cetonas"
    ],
    "fezes": [
        "Parasitológico", "Sangue oculto", "Rotavírus", "Coprocultura/Cultura de Fezes"
    ]
}
