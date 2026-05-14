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
 
# Correct frontend path — points to pages/ where all HTML files live
frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "pages"
 
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
    return RedirectResponse(url="/login.html")
 
# Serve frontend static files
app.mount(
    "/",
    StaticFiles(directory=frontend_path, html=True),
    name="static"
)
 