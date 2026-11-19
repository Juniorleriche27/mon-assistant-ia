import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = BASE_DIR.parent.parent
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(BASE_DIR / "storage")))

def resolve_file(filename: str) -> Path:
    candidates = [
        BASE_DIR / filename,
        BASE_DIR.parent / filename,
        WORKSPACE_ROOT / filename,
        Path("/app") / filename
    ]
    for c in candidates:
        if c.exists():
            return c
    return BASE_DIR / filename

MANUSCRIPT_PATH = resolve_file("Manuscrit_Complet_Assistant_IA_RAG.md")
PUBLIC_EXTRAIT_PATH = resolve_file("KORYXA_Assistant_IA_Extrait.pdf")

class Settings:
    BASE_DIR: Path = BASE_DIR
    WORKSPACE_ROOT: Path = WORKSPACE_ROOT
    STORAGE_DIR: Path = STORAGE_DIR
    MANUSCRIPT_PATH: Path = MANUSCRIPT_PATH
    PUBLIC_EXTRAIT_PATH: Path = PUBLIC_EXTRAIT_PATH

    # Passerelle KORYXA Pay
    KORYXA_PAY_BASE_URL: str = os.getenv("KORYXA_PAY_BASE_URL", "https://api-pay.koryxa.fr").rstrip("/")
    KORYXA_PAY_PROJECT_CODE: str = os.getenv("KORYXA_PAY_PROJECT_CODE", "koryxa-formation")
    KORYXA_PAY_PROJECT_KEY: str = os.getenv("KORYXA_PAY_PROJECT_KEY", "")
    KORYXA_WEBHOOK_SECRET: str = os.getenv("KORYXA_WEBHOOK_SECRET", "")
    
    # Produit & Tarification
    PRODUCT_CODE: str = "koryxa-assistant-ia"
    PRODUCT_NAME: str = "Créer et livrer son premier assistant IA — Pack Complet"
    PRODUCT_AMOUNT_XOF: int = 11000  # 11 000 FCFA
    PRODUCT_CURRENCY: str = "XOF"
    
    # Sécurité & Tokens
    SECRET_KEY: str = os.getenv("SECRET_KEY", "koryxa_tunnel_secure_key_2026_dev_prod_guard")
    ADMIN_SECRET_TOKEN: str = os.getenv("ADMIN_SECRET_TOKEN", "koryxa_admin_secret_token_18nov2026")
    
    # Cohere AI
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    COHERE_MODEL: str = os.getenv("COHERE_MODEL", "command-r-08-2024")

    # Moteur IA KNOWLIA (Moteur d'IA KORYXA)
    KNOWLIA_BASE_URL: str = os.getenv("KNOWLIA_BASE_URL", "").rstrip("/")
    KNOWLIA_API_KEY: str = os.getenv("KNOWLIA_API_KEY", "")
    KNOWLIA_TENANT_ID: str = os.getenv("KNOWLIA_TENANT_ID", "mon-assistant-ia")
    
    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/koryxa_tunnel.db")
    
    # Frontend Base URL
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

settings = Settings()
