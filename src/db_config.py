import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from project root
load_dotenv(BASE_DIR / ".env")


def get_database_engine():

    username = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")

    if not username or not password:
        raise ValueError("MySQL credentials not found in .env file")

    database_url = URL.create(
        drivername="mysql+pymysql",
        username=username,
        password=password,
        host="localhost",
        port=3306,
        database="olist_analytics"
    )

    return create_engine(database_url)