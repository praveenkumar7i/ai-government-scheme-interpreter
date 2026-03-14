from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Government Scheme Interpreter"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/schemes"
    chroma_persist_dir: str = "./vector_db/chroma_data"
    upload_dir: str = "./data/uploads"
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    sarvam_api_key: str = ""
    sarvam_base_url: str = "https://api.sarvam.ai"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
