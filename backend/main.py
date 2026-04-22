from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Import all models so SQLAlchemy can create their tables
from models import user, menu, order, reservation

app = FastAPI(title="Cafe Management API", version="1.0.0")

# CORS — allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Cafe Management API is running ✅"}
