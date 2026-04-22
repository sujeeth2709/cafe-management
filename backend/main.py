from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Import all models so SQLAlchemy creates tables
from models import user, menu, order, reservation

# Import all routers
from routers import auth, menu as menu_router, orders, reservations, admin, cart

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

# Register all routers
app.include_router(auth.router)
app.include_router(menu_router.router)
app.include_router(orders.router)
app.include_router(reservations.router)
app.include_router(admin.router)
app.include_router(cart.router)


@app.get("/")
def root():
    return {"message": "Cafe Management API is running ✅"}
