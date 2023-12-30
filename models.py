from sqlalchemy import Boolean, Column, Index, Integer, String

from database import Base


# Definieer de database tabel voor taken
class Present(Base):
    __tablename__ = "Presents"

    # Kolommen voor de takentabel
    id = Column(Integer, primary_key=True, index=True)  # ID van cadeau, is de primaire sleutel
    name = Column(String)  # Naam van cadeau
    category = Column(String)  # Category waar het cadeau zich in bevindt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
