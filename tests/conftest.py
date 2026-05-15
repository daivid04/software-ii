import pytest
import sys
import os
from pathlib import Path

# Agregar el proyecto al path (como lo hacen los tests unitarios)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Agregar el backend directamente para que 'db' sea accesible como módulo
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))
