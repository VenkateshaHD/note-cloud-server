from datetime import date
from app.models import models
from fastapi import APIRouter, HTTPException, Depends,Form
from sqlalchemy.orm import Session
from app.schemas import schema
from app.schemas.schema import UserCreate
from app.core import security
from app import database
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
def register(request: UserCreate,db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.email == request.email).first()
    if existing:
        # raise HTTPException(status_code=400, detail="Email already registered")
        return {"status": 0,"message":"Email already registered"}

    hashed = security.hash_password(request.password)
    # return {"status": 0,"message":hashed}
    db_user = models.User(email=request.email, hashed_password=hashed, name=request.name, created_at=str(date.today()))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = security.create_token({"sub": db_user.email})
    return {"status":1,"access_token": token,"user":{"id":db_user.id,"email":db_user.email,"name":db_user.name}}

@router.post("/login")
def login(request: schema.UserCredentials, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user or not security.verify_password(request.password, user.hashed_password):
        # raise HTTPException(status_code=400, detail="Invalid credentials")
        return {"status": 0,"message":"Invalid credentials"}

    token = security.create_token({"sub": user.email})
    return {"status": 1,"token": token,"user":{"id":user.id,"email":user.email,"name":user.name}}

@router.get("/get-all-users",)
def get_all_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()