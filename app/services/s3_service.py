import os
import boto3
from dotenv import load_dotenv, find_dotenv
from botocore.exceptions import BotoCoreError, ClientError

load_dotenv(find_dotenv('app/config/.env'))


def get_s3_client():
    """Carrega as credenciais do .env e retorna um cliente S3 configurado."""
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_bucket_name = os.getenv("AWS_BUCKET_NAME")
    aws_region = os.getenv("AWS_REGION")

    if not all([aws_access_key_id, aws_secret_key, aws_bucket_name, aws_region]):
        raise ValueError("Variáveis de ambiente do AWS não foram carregadas corretamente.")

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )


def get_pdf_from_s3(exams_json: dict, download_folder: str = "downloads/") -> str:
    """
    Obtém o caminho do arquivo PDF no S3 a partir do JSON fornecido e faz o download.

    :param exams_json: Dicionário contendo os dados do exame, incluindo "storage_path".
    :param download_folder: Pasta local onde o arquivo será salvo.
    :return: Caminho local do arquivo baixado.
    """
    s3_client = get_s3_client()
    file_name = exams_json.get("storage_path")

    if not file_name:
        raise ValueError("O JSON não contém um 'storage_path' válido.")

    try:
        # Remover a primeira pasta "vivahcare_files/"
        file_name_without_root = '/'.join(file_name.split('/')[1:])

        full_download_folder = os.path.join(download_folder, os.path.dirname(file_name_without_root))
        os.makedirs(full_download_folder, exist_ok=True)

        local_file_path = os.path.join(download_folder, file_name_without_root)

        bucket_name = os.getenv("AWS_BUCKET_NAME")

        s3_client.download_file(bucket_name, file_name_without_root, local_file_path)

        print(f"Arquivo {file_name_without_root} baixado com sucesso para {local_file_path}")
        return local_file_path

    except (BotoCoreError, ClientError) as e:
        print(f"Erro ao baixar {file_name} do S3: {str(e)}")
        raise


def list_s3_files():
    """
    Lista os arquivos dentro do bucket S3.
    """
    s3_client = get_s3_client()  # Criando cliente S3

    try:
        bucket_name = os.getenv("AWS_BUCKET_NAME")  # Pegando o nome do bucket

        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            return [obj["Key"] for obj in response["Contents"]]
        else:
            return []

    except (BotoCoreError, ClientError) as e:
        print(f"Erro ao listar arquivos do S3: {str(e)}")
        return []