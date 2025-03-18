from functools import lru_cache
from pydantic import BaseModel

class Settings(BaseModel):
    """Configurações da aplicação usando variáveis de ambiente."""
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket_name: str
    aws_region: str

    @classmethod
    def from_env(cls):
        """Carrega as configurações a partir das variáveis de ambiente."""
        import os
        from dotenv import load_dotenv
        load_dotenv('app/config/.env')
        
        return cls(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            aws_bucket_name=os.getenv("AWS_BUCKET_NAME", ""),
            aws_region=os.getenv("AWS_REGION", "")
        )

@lru_cache()
def get_settings():
    return Settings.from_env()
