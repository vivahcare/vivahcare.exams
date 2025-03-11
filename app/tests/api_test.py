from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "VivahCare API is running!"}


@app.get("/exams")
def test(file_name: int):
    """
    Rota que recebe o nome do arquivo PDF, busca no S3, extrai o texto e processa com IA.
    """

    return {'nome': file_name}