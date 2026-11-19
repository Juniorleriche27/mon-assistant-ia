import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Customer, DownloadLog, Order

router = APIRouter(prefix="/api/v1/downloads", tags=["Téléchargements"])

PROTECTED_ASSETS = {
    "livre": {
        "filename": "Creer_et_livrer_son_premier_assistant_IA_Cohere.pdf",
        "media_type": "application/pdf",
        "display_name": "Livre - Créer et livrer son premier assistant IA (Cohere).pdf"
    },
    "projet": {
        "filename": "Assistant_IA_RAG_Cohere_Projet.zip",
        "media_type": "application/zip",
        "display_name": "Code et supports - Horizon Numerique.zip"
    }
}

@router.get("/extrait-gratuit")
def download_free_sample():
    """
    Téléchargement public direct de l'extrait gratuit (Lead Magnet).
    """
    path = settings.PUBLIC_EXTRAIT_PATH
    if not path.exists():
        # Fallback si déplacé dans storage ou public
        fallback = settings.BASE_DIR.parent / "tunnel" / "frontend" / "public" / "KORYXA_Assistant_IA_Extrait.pdf"
        if fallback.exists():
            path = fallback
        else:
            raise HTTPException(status_code=404, detail="Extrait gratuit momentanément indisponible")

    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename="KORYXA_Assistant_IA_Extrait.pdf"
    )

@router.get("/pack/{asset_key}")
def download_protected_asset(
    asset_key: str,
    request: Request,
    email: str = Query(..., description="Email de l'acheteur"),
    order_id: str = Query(..., description="ID de la commande"),
    db: Session = Depends(get_db),
):
    """
    Téléchargement sécurisé et contrôlé des fichiers du pack complet.
    Interdit à tout visiteur sans commande confirmée 'succeeded'.
    """
    if asset_key not in PROTECTED_ASSETS:
        raise HTTPException(status_code=404, detail="Livrable non reconnu")

    # 1. Vérification du client
    customer = db.query(Customer).filter(Customer.email == email.strip().lower()).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit : compte introuvable")

    # 2. Vérification des droits d'accès et du statut de paiement
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.customer_id == customer.id,
        Order.status == "succeeded"
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit : aucun paiement confirmé pour cette commande"
        )

    # 3. Récupération du fichier dans le répertoire protégé
    asset_info = PROTECTED_ASSETS[asset_key]
    file_path = settings.STORAGE_DIR / asset_info["filename"]

    if not file_path.exists():
        raise HTTPException(status_code=500, detail="Fichier introuvable sur le serveur de stockage")

    # 4. Enregistrement télémétrique du téléchargement
    client_ip = request.client.host if request.client else "unknown"
    log_entry = DownloadLog(
        customer_id=customer.id,
        asset_name=asset_key,
        ip_address=client_ip
    )
    db.add(log_entry)
    db.commit()

    return FileResponse(
        path=str(file_path),
        media_type=asset_info["media_type"],
        filename=asset_info["display_name"]
    )
