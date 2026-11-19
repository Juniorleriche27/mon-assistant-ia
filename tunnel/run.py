import sys
from pathlib import Path
import uvicorn

# Ajout du dossier backend au PYTHONPATH
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("Démarrage du Tunnel de Vente & Espace Client KORYXA sur http://localhost:8000 ...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
