from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
import auth
from database import SessionLocal, engine
import os

if not os.path.exists('./sqlitedb'):
    os.makedirs('./sqlitedb')

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ------------------------------ POST Functions ------------------------------

# Endpoint om een nieuw cadeau toe te voegen
@app.post("/cadeau", response_model=schemas.Present)
def add_present(present: schemas.AddPresent, db: Session = Depends(get_db)):
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
@app.get("/cadeaus/category/{category:str}", response_model=List[schemas.Present])
def get_present_names_by_category(category: str, db: Session = Depends(get_db)):
    present = crud.get_present_names_by_category(db=db, category=category)
    if not present:
        raise HTTPException(status_code=404, detail=f"Geen cadeaus gevonden in de categorie {category}")
    return present


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
def delete_present(present_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.delete_present_by_id(db, present_id=present_id)


# Endpoint om alle cadeaus te verwijderen
@app.delete("/cadeaus", response_model=str)
def delete_all_presents(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    crud.delete_all_presents(db)
    return "Alle cadeaus zijn verwijderd!"


# ------------------------------ USER Functions ------------------------------

# Nieuwe user aanmaken
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail is al geregistreerd!")
    return crud.create_user(db=db, user=user)


# Alle gebruikers verwijderen
@app.delete("/users", response_model=str)
def delete_all_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):  # BEVEILIGD
    crud.delete_all_users(db)
    return "Alle gebruikers zijn verwijderd!"


# ------------------------------ oAuth Functions ------------------------------
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Proberen om de user te authentiseren
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    # Return JWT als bearer token om in de headers geplaatst te worden
    return {"access_token": access_token, "token_type": "bearer"}
