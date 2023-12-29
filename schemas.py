from pydantic import BaseModel


# Basismodel voor een taak met optionele naam en een voltooide vlag
class PresentBase(BaseModel):
    name: str | None = None  # Naam van de taak, kan niet optioneel zijn
    completed: bool  # Veld dat aangeeft of de taak is voltooid of niet


# Model voor het maken van een nieuwe taak, overerft van TaskBase
class addPresent(PresentBase):
    pass


# Task-model dat wordt teruggestuurd door de API, heeft een ID en de attributen van TaskBase
class Present(PresentBase):
    id: int  # ID van de taak

    # Configuratie om te kunnen werken met SQLAlchemy ORM
    class Config:
        orm_mode = True
