from pydantic import BaseModel
from typing import Optional

# ---------- Note Schemas ----------
class NoteBase(BaseModel):
    title: str
    content: Optional[str] = ""
    is_public: Optional[bool] = False

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    file_url: Optional[str] = None

    class Config:
        orm_mode = True

# ---------- User Schemas ----------
class UserCreate(BaseModel):
    email: str
    password: str

# ---------- Token Schema ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
