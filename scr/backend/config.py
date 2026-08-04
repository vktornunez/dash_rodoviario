import os

class Settings:
    PROJECT_NAME: str = "Dashboard PRF 2025 API"
    PROJECT_VERSION: str = "1.0.0"
    
    DB_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME: str = os.getenv("POSTGRES_DB", "prf_db")
    DB_USER: str = os.getenv("POSTGRES_USER", "prf_user")
    DB_PASS: str = os.getenv("POSTGRES_PASSWORD", "prf_pass")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
