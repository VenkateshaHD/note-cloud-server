from datetime import date, datetime
from app.core.s3 import upload_to_s3
from app.models import models
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import schema
from app.core import security
from app.schemas.schema import NoteCreate, NoteOut
from fastapi import File, UploadFile
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

@router.get("/")
def list_notes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # return db.query(models.Note).filter(models.Note.owner_id == current_user.id).all()
    return db.query(models.Note).all()

@router.post("/add")
def create_note_with_file(
    title: str = Form(...),
    content: str = Form(""),
    isPublic: bool = Form(False),
    files: UploadFile = File(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    file_url = None

    if files:
        print(files.filename)
        s3_key = f"{datetime.now()}-{current_user.id}-{files.filename}"
        file_url = upload_to_s3(files, s3_key)  # This should return the CloudFront link

    note = models.Note(
        title=title,
        content=content,
        is_public=isPublic,
        file_url=file_url,
        owner_id=current_user.id,
        created_at=str(datetime.today()),
        updated_at=str(datetime.today())
    )

    db.add(note)
    db.commit()
    db.refresh(note)
    return {"status": 1, "message": "Note created successfully", "note":  note}

@router.put("/{note_id}")
def update_note(note_id: int,  
    title: str = Form(...),
    content: str = Form(""),
    files: UploadFile = File(None), 
    db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found or You are Not a owner of this note")
    
    db_note.title = title
    db_note.content = content

    if files:
        print(files.filename)
        s3_key = f"{datetime.now()}-{current_user.id}-{files.filename}"
        file_url = upload_to_s3(files, s3_key)  # This should return the CloudFront link
        db_note.file_url = file_url
    # db_note.is_public = note.isPublic
    db_note.updated_at = str(datetime.today())
    db.commit()
    db.refresh(db_note)
    return {"status":1,"data":db_note}

# @router.post("/add", response_model=schema.NoteOut)
# def create_note(note: schema.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
#     new_note = models.Note(**note.dict(), owner_id=current_user.id)
#     db.add(new_note)
#     db.commit()
#     db.refresh(new_note)
#     return new_note

@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or You are Not a owner of this note")
    db.delete(note)
    db.commit()
    return {"status": 1, "message": "Note deleted successfully"}
