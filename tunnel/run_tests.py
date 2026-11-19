import os
import sys
import unittest
from pathlib import Path

backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("Exécution des tests automatisés du Tunnel KORYXA...")
    loader = unittest.TestLoader()
    suite = loader.discover(str(backend_dir / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
