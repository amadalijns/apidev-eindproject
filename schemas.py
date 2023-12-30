from pydantic import BaseModel, validator
from typing import List


# Basismodel voor een cadeau
class PresentBase(BaseModel):
    name: str  # Naam van het cadeau
    category: str  # Categorie van het cadeau


# Model voor het maken van een nieuwe cadeau, erft over van PresentBase
class AddPresent(PresentBase):
    pass


# Model voor het updaten van een cadeau, erft over van PresentBase
class PresentUpdate(PresentBase):
    name: str | None = None
    category: str | None = None


# Model voor het cadeau met ID, erft van PresentBase
class Present(PresentBase):
    id: int  # ID van het cadeau

    class Config:
        orm_mode = True


# Model voor de lijst van namen
class PresentName(BaseModel):
    name: str

    class Config:
        orm_mode = True


# Model voor de lijst van namen
class PresentNameList(BaseModel):
    names: List[PresentName]

    class Config:
        orm_mode = True


# Model voor het maken van een nieuwe gebruiker
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
