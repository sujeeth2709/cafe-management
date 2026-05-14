from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path

from routers import auth
from routers import menu as menu_router
from routers import orders
from routers import reservations
from routers import admin
from routers import cart

app = FastAPI(
    title="Cafe Management API",
    version="1.0.0"
)

# CORS - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base frontend path
frontend_path = Path(__file__).resolve().parent.parent / "frontend"

# Register API routers
app.include_router(auth.router)
app.include_router(menu_router.router)
app.include_router(orders.router)
app.include_router(reservations.router)
app.include_router(admin.router)
app.include_router(cart.router)

# Redirect root to login page
@app.get("/")
def root():
    return RedirectResponse(url="/pages/login.html")

# Mount styles, scripts, components so ../styles and ../scripts resolve correctly
app.mount("/styles", StaticFiles(directory=frontend_path / "styles"), name="styles")
app.mount("/scripts", StaticFiles(directory=frontend_path / "scripts"), name="scripts")
app.mount("/components", StaticFiles(directory=frontend_path / "components"), name="components")

# Serve all pages under /pages/
app.mount("/pages", StaticFiles(directory=frontend_path / "pages", html=True), name="pages")

# Fallback: serve entire frontend
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
