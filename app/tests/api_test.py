import json
import requests

url = "https://api.vivahcare.com/exams/update"

data = {
  "date": "2025-03-17",
  "exams": [
    {
                "id": "3ab95d50-d111-449c-8f95-e105b70741c2",
                "type": "ROTINA DE URINA (EQU - M)",
                "method": "Físico-Químico e Microscopia",
                "categories": [
                    {
                        "name": "EXAME FÍSICO",
                        "fields": [
                            {
                                "field": "Densidade",
                                "label": "Densidade",
                                "values": [
                                    {
                                        "value": "1,015",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "pH",
                                "label": "pH",
                                "values": [
                                    {
                                        "value": "5,0",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Volume",
                                "label": "Volume",
                                "values": [
                                    {
                                        "value": "70,0",
                                        "unit_measure": "mL",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Depósito",
                                "label": "Depósito",
                                "values": [
                                    {
                                        "value": "Pequeno",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Aspecto",
                                "label": "Aspecto",
                                "values": [
                                    {
                                        "value": "Ligeiramente turvo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Cor",
                                "label": "Cor",
                                "values": [
                                    {
                                        "value": "Amarelo claro",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            }
                        ]
                    },
                    {
                        "name": "EXAME QUÍMICO",
                        "fields": [
                            {
                                "field": "Proteínas",
                                "label": "Proteínas",
                                "values": [
                                    {
                                        "value": "Negativo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Glicose",
                                "label": "Glicose",
                                "values": [
                                    {
                                        "value": "Normal",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Corpos Cetônicos",
                                "label": "Corpos Cetônicos",
                                "values": [
                                    {
                                        "value": "Negativo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Hemoglobina",
                                "label": "Hemoglobina",
                                "values": [
                                    {
                                        "value": "Negativo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Esterase de leucócitos",
                                "label": "Esterase de leucócitos",
                                "values": [
                                    {
                                        "value": "Negativo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Bilirrubina",
                                "label": "Bilirrubina",
                                "values": [
                                    {
                                        "value": "Negativo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Urobilinogênio",
                                "label": "Urobilinogênio",
                                "values": [
                                    {
                                        "value": "Normal",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Nitritos",
                                "label": "Nitritos",
                                "values": [
                                    {
                                        "value": "Negativo",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            }
                        ]
                    },
                    {
                        "name": "EXAME MICROSCÓPICO",
                        "fields": [
                            {
                                "field": "Células epiteliais",
                                "label": "Células epiteliais",
                                "values": [
                                    {
                                        "value": "Algumas (2 por campo)",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Leucócitos",
                                "label": "Leucócitos",
                                "values": [
                                    {
                                        "value": "Raros (01 por campo)",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Eritrócitos",
                                "label": "Eritrócitos",
                                "values": [
                                    {
                                        "value": "Raros (01 por campo)",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Filamentos de muco",
                                "label": "Filamentos de muco",
                                "values": [
                                    {
                                        "value": "Poucos",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            },
                            {
                                "field": "Bacteriúria",
                                "label": "Bacteriúria",
                                "values": [
                                    {
                                        "value": "Discreta",
                                        "unit_measure": "",
                                        "value_type": "string",
                                        "reference": {}
                                    }
                                ],
                                "type": "input"
                            }
                        ]
                    }
                ]
            }
  ]
}
json_data = json.dumps(data)

response = requests.post(url, data = data)

print(response.status_code)

# if response.status_code == 200:
#     print(response.json())  # Se a resposta for JSON
# else:
#     print(f"Erro: {response.status_code}")