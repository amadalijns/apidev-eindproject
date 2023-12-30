from sqlalchemy import Boolean, Column, Index, Integer, String

from database import Base


# Model voor cadeaus met ID, naam en categorie
class Present(Base):
    __tablename__ = "Presents"

    # Kolommen in de presents-tabel
    id = Column(Integer, primary_key=True, index=True)  # ID van cadeau, is de primaire sleutel
    name = Column(String)  # Naam van cadeau
    category = Column(String)  # Categorie waar het cadeau zich in bevindt


# Model voor users met ID, email en wachtwoord
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # ID van user, is de primaire sleutel
    email = Column(String, unique=True, index=True)  # email om in te loggen
    hashed_password = Column(String)  # wachtwoord van de user
