from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Omnichannel"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list = ["*"]
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_HOST: str = "smtp.example.com"
      EMAIL_PORT: int = 587
      EMAIL_USERNAME: str = "your-email@example.com"
      EMAIL_PASSWORD: str = "your-email-password"
      EMAIL_HOST: str = "smtp.example.com"
      EMAIL_PORT: int = 587
      EMAIL_USERNAME: str = "your-email@example.com"
      EMAIL_PASSWORD: str = "your-email-password"
      EMAIL_FROM: str = "noreply@example.com" = "noreply@example

    class Config:
        case_sensitive = True

settings = Settings()