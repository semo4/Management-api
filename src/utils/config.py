import os

from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")


def get_database_url():
    """It will Generate Database URL for PostgreSQL To connect with

    Returns:
        string: Database Url to open connection with it
    """
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
