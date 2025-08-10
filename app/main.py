from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, notes, upload
from app.database import Base, engine

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Creating database tables...")

# Base.metadata.create_all(bind=engine)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}