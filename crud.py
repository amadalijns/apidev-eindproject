from sqlalchemy.orm import Session

import models
import schemas


# ------------------------------ GET Functions ------------------------------

# Functie om alle cadeaus op te halen
def get_presents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Present).offset(skip).limit(limit).all()


# Functie om een cadeau op te halen op basis van ID
def get_present_by_id(db: Session, present_id: int):
    return db.query(models.Present).filter(models.Present.id == present_id).first()


# Functie om een cadeau op te halen op basis van naam
def get_present_by_name(db: Session, name: str):
    return db.query(models.Present).filter(models.Present.name == name).first()


# Functie om een cadeau op te halen op basis van category
def get_present_names_by_category(db: Session, category: str):
    return db.query(models.Present.name).filter(models.Present.category == category).all()


# ------------------------------ POST Functions ------------------------------

# Functie om een nieuw cadeau te maken en op te slaan in de database
def add_present(db: Session, present: schemas.Present):
    db_present = models.Present(**present.dict())
    db.add(db_present)
    db.commit()
    db.refresh(db_present)
    return db_present


# ------------------------------ PUT Functions ------------------------------

# Functie om cadeau bij te werken op basis van ID
def update_present(db: Session, present_id: int, present: schemas.PresentUpdate):
    db_present = db.query(models.Present).filter(models.Present.id == present_id).first()
    if db_present:
        db_present.name = present.name
        db_present.category = present.category
        db.commit()
        db.refresh(db_present)
    return db_present


# ------------------------------ DELETE Functions ------------------------------

# Functie om een cadeau te verwijderen op basis van ID
def delete_present_by_id(db: Session, present_id: int):
    present = db.query(models.Present).filter(models.Present.id == present_id).first()
    if present:
        db.delete(present)
        db.commit()
        return {"message": f"Cadeau {present_id} is verwijderd!"}
    return {"message": f"Cadeau {present_id} niet gevonden!"}


# Functie om alle cadeaus te verwijderen
def delete_all_presents(db: Session):
    db.query(models.Present).delete()
    db.commit()
    return {"message": "Alle cadeaus zijn verwijderd!"}
