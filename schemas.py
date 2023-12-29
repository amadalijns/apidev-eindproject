from pydantic import BaseModel
from typing import List


# Basismodel voor een cadeau met optionele naam en category
class PresentBase(BaseModel):
    name: str  # Naam van het cadeau
    category: str  # Category van het cadeau


# Model voor het maken van een nieuwe cadeau, overerft van PresentBase
class addPresent(PresentBase):
    pass


# Model voor het updaten van een cadeau, overerft van PresentBase
class PresentUpdate(PresentBase):
    name: str | None = None
    category: str | None = None


# Model voor het teruggestuurde cadeau met ID, erft van PresentBase
class Present(PresentBase):
    id: int  # ID van het cadeau

    # Configuratie om te kunnen werken met SQLAlchemy ORM
    class Config:
        orm_mode = True


# Model voor het teruggestuurde lijst van cadeau-namen
class PresentName(BaseModel):
    name: str

    class Config:
        orm_mode = True


# Model voor het teruggestuurde lijst van cadeau-namen
class PresentNameList(BaseModel):
    names: List[PresentName]

    class Config:
        orm_mode = True
