# config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ganti sesuai koneksi database PostgreSQL Anda di DBeaver
# Format: postgresql://user:password@localhost:5432/nama_database
DATABASE_URL = "postgresql://postgres:Huangrenjun23.@localhost:5433/data_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()