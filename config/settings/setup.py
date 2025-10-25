import argparse
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

from common.aws.secrets import fetch_secrets

class AppSettings(BaseSettings):
    """
    Application settings loaded from .env files.
    """
    # [.ENV]
    APP__PORT: str
    APP__TITLE: str
    APP__DESCRIPTION: str
    APP__VERSION: str
    APP__OPENAPI_URL: str
    APP__DOCS_URL: str
    APP__REDOC_URL: str

    AWS_SM__SECRET_NAME_PG: str # AWS Secrets Manager - Secret name for postgres credentials
    AWS_RDS__DB_NAME_PG: str # AWS RDS - Database credentials for postgres

    async def load_pg_creds(self):
        secret_id = self.AWS_SM__SECRET_NAME_PG

        if not secret_id:
            raise RuntimeError("AWS_SM__SECRET_NAME_PG is not set")
        
        pg_creds = await fetch_secrets(secret_id=secret_id)

        self.DB_USERNAME_PG = pg_creds.get("username")
        self.DB_PASS_PG = pg_creds.get("password")
        self.DB_HOST_PG = pg_creds.get("host")
        self.DB_PORT_PG = int(pg_creds.get("port"))

    def detect_env_file() -> str:
        """
        Detect the .env file to load based on CLI args:
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--env", default=None, help="Application environment (dev/prod)")
        parser.add_argument("--env-file", default=None, help="Explicit .env file path")

        # Parse known args safely (ignore unrelated ones like Uvicorn's)
        args, _ = parser.parse_known_args(sys.argv[1:])

        # 1 explicit --env-file
        if args.env_file:
            print(f"[INFO] Using explicit env file: {args.env_file}")
            return args.env_file

        # 2 mapped env name
        env_mapping = {
            "local": ".env",
            "dev": ".env.dev",
            "prod": ".env.prod",
        }

        if args.env:
            env_file = env_mapping.get(args.env.lower(), ".env")
            print(f"[INFO] Using env file from --env-file ({args.env}): {env_file}")
            return env_file

        # Fallback: default
        print("[INFO] Using default Dev environment `.env` file")
        return ".env"

    # Pydantic config
    model_config = SettingsConfigDict(env_file=detect_env_file(), extra="allow")