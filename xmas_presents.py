from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

app = FastAPI()

# Creëer de database tabellen
models.Base.metadata.create_all(bind=engine)


# Functie om de database sessie op te halen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------ POST Functions ------------------------------

# Endpoint om een nieuw cadeau toe te voegen
@app.post("/cadeau", response_model=schemas.Present)
def add_present(present: schemas.addPresent, db: Session = Depends(get_db)):

    # Controleren of het cadeau al bestaat op basis van de naam
    db_present = crud.get_present_by_name(db, name=present.name)
    if db_present:
        raise HTTPException(status_code=400, detail="Een cadeau met deze naam bestaat al!")
    return crud.add_present(db, present)


# ------------------------------ GET Functions ------------------------------

# Endpoint om alle cadeaus op te halen
@app.get("/cadeaus", response_model=list[schemas.Present])
def read_presents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_presents(db, skip=skip, limit=limit)


# Endpoint om een specifiek cadeau op te halen op basis van ID
@app.get("/cadeaus/{present_id}", response_model=schemas.Present)
def read_present(present_id: int, db: Session = Depends(get_db)):
    present = crud.get_present_by_id(db, present_id=present_id)
    if present is None:
        raise HTTPException(status_code=404, detail=f"Cadeau {present_id} is niet gevonden!")
    return present


# Endpoint om een specifiek cadeau op te halen op basis van category
# @app.get("/cadeaus/{category:str}", response_model=schemas.PresentNameList)
# def get_present_names_by_category(category: str, db: Session = Depends(get_db)):
#     names = crud.get_present_names_by_category(db=db, category=category)
#     if not names:
#         raise HTTPException(status_code=404, detail=f"Geen cadeaus gevonden met categorie {category}")
#     return {"names": names}


# ------------------------------ PUT Functions ------------------------------

# Endpoint om een cadeau bij te werken
@app.put("/cadeaus/{present_id}")
def update_present(present_id: int, present: schemas.PresentUpdate, db: Session = Depends(get_db)):

    db_present = crud.update_present(db, present_id, present)
    if db_present is None:
        raise HTTPException(status_code=404, detail=f"Cadeau {present_id} is niet gevonden!")
    return db_present


# ------------------------------ DELETE Functions ------------------------------

# Endpoint om een cadeau te verwijderen op basis van ID
@app.delete("/cadeaus/{present_id}")
def delete_present(present_id: int, db: Session = Depends(get_db)):
    return crud.delete_present_by_id(db, present_id=present_id)


# Endpoint om alle cadeaus te verwijderen
@app.delete("/cadeaus")
def delete_presents(db: Session = Depends(get_db)):
    return crud.delete_all_presents(db)
