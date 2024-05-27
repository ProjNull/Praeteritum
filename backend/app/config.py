import dotenv
import os

dotenv.load_dotenv()

DB_DRIVER: str = os.environ.get("DB_DRIVER", "postgresql")
DB_HOST: str = os.environ.get("DB_HOST", "postgres")
DB_PORT: str = os.environ.get("DB_PORT", "5432")
DB_USER: str = os.environ.get("DB_USER", "prae")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "password")
DB_NAME: str = os.environ.get("DB_NAME", "prae")
CACHE_HOST: str = os.environ.get("CACHE_HOST", "redis")
CACHE_PORT: str = os.environ.get("CACHE_PORT", "6379")
