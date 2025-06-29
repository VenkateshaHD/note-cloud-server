from app.models import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import schema
from app.core import security
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[schema.NoteOut])
def list_notes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Note).filter(models.Note.owner_id == current_user.id).all()

@router.post("/", response_model=schema.NoteOut)
def create_note(note: schema.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_note = models.Note(**note.dict(), owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/{note_id}", response_model=schema.NoteOut)
def get_note(note_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
