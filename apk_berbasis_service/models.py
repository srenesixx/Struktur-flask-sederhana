from sqlalchemy import Column, String, Text, Date
from config import Base

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    nim = Column(String, primary_key=True, unique=True, nullable=False)
    nama = Column(String, nullable=False)
    tahun_masuk = Column(String(4), nullable=False)
    alamat = Column(Text)
    tanggal_lahir = Column(Date)
