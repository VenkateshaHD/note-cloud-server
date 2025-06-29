from app.models import models
from fastapi import APIRouter, HTTPException, Depends,Form
from sqlalchemy.orm import Session
from app.schemas import schema
from app.core import security
from app import database
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=schema.Token)
def register(email: str = Form(...),password:str = Form(...), db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = security.hash_password(password)
    db_user = models.User(email=email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = security.create_token({"sub": db_user.email})
    return {"access_token": token}

@router.post("/login", response_model=schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = security.create_token({"sub": user.email})
    return {"access_token": token}

@router.get("/get-all-users",)
def get_all_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()
