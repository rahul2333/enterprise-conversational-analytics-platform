import os

class Settings:
    app_env = os.getenv("APP_ENV","local")
    llm_provider = os.getenv("LLM_PROVIDER","stub")
    vector_provider = os.getenv("VECTOR_PROVIDER","stub")
    bq_project = os.getenv("BQ_PROJECT")
    bq_dataset = os.getenv("BQ_DATASET")

settings = Settings()
