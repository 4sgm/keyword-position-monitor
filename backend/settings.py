from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Server
    APP_NAME: str = "Keyword Position Monitor"
    DEBUG: bool = True

    # Keyword.com API
    KEYWORD_COM_BASE_URL: str = "https://api.keyword.com/v2"
    KEYWORD_COM_API_KEY: str = ""
    # Some providers use "Bearer", some use "Token". Check docs.keyword.com to confirm your account's scheme.
    KEYWORD_COM_AUTH_SCHEME: str = "Bearer"
    # Header name to carry the token. Often "Authorization", sometimes "X-API-Key".
    KEYWORD_COM_AUTH_HEADER: str = "Authorization"

    # Endpoint paths (customizable in case of API changes or account-specific paths)
    # Update these to the exact paths from https://docs.keyword.com/
    ENDPOINT_LIST_PROJECTS: str = "/projects"
    ENDPOINT_CREATE_PROJECT: str = "/projects"
    ENDPOINT_LIST_PROJECT_KEYWORDS: str = "/projects/{project_id}/keywords"
    ENDPOINT_ADD_KEYWORDS: str = "/projects/{project_id}/keywords"
    ENDPOINT_GET_KEYWORD_HISTORY: str = "/keywords/{keyword_id}/history"  # expected to return SERP/rank history
    ENDPOINT_REFRESH_SERP: str = "/projects/{project_id}/refresh"

    # Polling / Scheduler
    SCHEDULE_CRON: str = "0 7 * * *"  # daily 07:00
    TIMEZONE: str = "America/Los_Angeles"

    # Database
    SQLITE_URL: str = "sqlite:///./monitor.db"

    # App auth (simple)
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()