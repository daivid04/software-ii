"""
Environment.py: Hooks de Behave para setup y teardown de pruebas BDD
Inicializa TestingAPI y limpia estado entre escenarios
"""

import sys
import os

# Agregar backend al path para importaciones
backend_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Verificar que el path está configurado
print(f"[INFO] PYTHONPATH: {backend_path}")

try:
    from testing.testing_api import TestingAPI
    print("[OK] TestingAPI importada exitosamente")
except ImportError as e:
    print(f"[ERROR] No se pudo importar TestingAPI: {e}")
    raise


def before_all(context):
    """Ejecuta antes de todos los escenarios."""
    print("[START] Iniciando suite BDD: Taller Diego MVP")


def before_scenario(context, scenario):
    """Ejecuta antes de cada escenario."""
    # Crear instancia nueva de TestingAPI para cada escenario
    context.testing_api = TestingAPI(use_memory_db=True)
    
    # Inicializar servicios catálogo
    context.testing_api.registrar_servicios_catalogo()
    
    print(f"  [SCENARIO] {scenario.name}")


def after_scenario(context, scenario):
    """Ejecuta después de cada escenario."""
    # Limpiar BD y cerrar sesión
    try:
        if hasattr(context, 'testing_api'):
            context.testing_api.close()
    except Exception as e:
        print(f"  [WARNING] Error al cerrar TestingAPI: {e}")


def after_all(context):
    """Ejecuta después de todos los escenarios."""
    print("[END] Suite BDD completada")
