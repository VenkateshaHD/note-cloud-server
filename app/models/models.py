from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# ---------- User Model ----------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    notes = relationship("Note", back_populates="owner")

# ---------- Note Model ----------
class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    file_url = Column(String(255), nullable=True)
    is_public = Column(Integer, default=0)  # 0 for private, 1 for public

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="notes")
