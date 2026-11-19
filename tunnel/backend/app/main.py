from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.admin_router import router as admin_router
from app.checkout_router import router as checkout_router
from app.client_router import router as client_router
from app.config import settings
from app.db import init_db
from app.downloads import router as downloads_router
from app.webhook import router as webhook_router

FRONTEND_DIR = settings.BASE_DIR.parent / "frontend"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation des tables SQLite au démarrage
    init_db()
    yield

app = FastAPI(
    title="KORYXA Tunnel & Espace Client API",
    description="API du tunnel de vente et de l'espace client pour 'Créer et livrer son premier assistant IA'",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes API
app.include_router(checkout_router)
app.include_router(webhook_router)
app.include_router(downloads_router)
app.include_router(client_router)
app.include_router(admin_router)

# Montage des fichiers statiques CSS, JS et Images
css_dir = FRONTEND_DIR / "css"
js_dir = FRONTEND_DIR / "js"
images_dir = FRONTEND_DIR / "images"
if css_dir.exists():
    app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
if js_dir.exists():
    app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
if images_dir.exists():
    app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")

# Pages HTML du tunnel de vente et de l'espace client
@app.get("/")
def get_sales_page():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Tunnel KORYXA Backend en ligne"}

@app.get("/commande/statut")
def get_order_status_page():
    statut_file = FRONTEND_DIR / "commande-statut.html"
    if statut_file.exists():
        return FileResponse(statut_file)
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/espace-client")
def get_client_portal_page():
    portal_file = FRONTEND_DIR / "espace-client.html"
    if portal_file.exists():
        return FileResponse(portal_file)
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/admin")
def get_admin_page():
    admin_file = FRONTEND_DIR / "admin.html"
    if admin_file.exists():
        return FileResponse(admin_file)
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "koryxa-tunnel-backend"}
