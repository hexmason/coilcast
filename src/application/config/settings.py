from pathlib import Path
from typing import Literal
from pydantic import AnyUrl, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_LOGIN: str = "admin"
    ADMIN_PASS: str = "changeme"
    MUSIC_FOLDER: Path = Path("./music")
    HTTP_PORT: int = 8080
    DEBUG_MODE: bool = False
    DB_TYPE: Literal["POSTGRESQL", "SQLITE"] = "SQLITE"
    DB_NAME: str = "coilcast"
    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DATABASE_URI: AnyUrl | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @staticmethod
    def _build_dsn(scheme: str, values: dict) -> str:
        return str(
            PostgresDsn.build(
                scheme=scheme,
                username=values.get("DB_USER"),
                password=values.get("DB_PASS"),
                host=values.get("DB_HOST"),
                port=int(values["DB_PORT"]) if values.get("DB_PORT") else None,
                path=values.get("DB_NAME"),
            )
        )

    @field_validator("DATABASE_URI")
    def assemble_db_connection(
            cls, v: str | None,
            info: ValidationInfo
    ) -> str:

        if isinstance(v, str):
            return v
        db_type = info.data.get("DB_TYPE")
        if db_type == "SQLITE":
            return f"sqlite+aiosqlite:///{info.data.get("DB_NAME")}.db"
        elif db_type == "POSTGRESQL":
            return cls._build_dsn("postgresql+asyncpg", info.data)
        raise ValueError("Unsupported database type")


settings = Settings()
