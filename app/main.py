from fastapi import FastAPI
from app.api import auth, notes, upload
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])


@app.get("/")
def read_root():
    return {"Hello": "World"}