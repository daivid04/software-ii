"""
Script de prueba para verificar la conexión a la base de datos
"""
import sys
sys.path.insert(0, 'e:/UNJBG/SEXTO CICLO 6/INGENIERIA DE SOFTWARE 1/PROYECTO/Taller-Diego/backend')

print("1. Importando configuración...")
from core.config import settings
print(f"   DATABASE_URL: {settings.DATABASE_URL[:50]}...")

print("\n2. Importando base de datos...")
from db.base import engine, SessionLocal
print("   ✓ Engine creado")

print("\n3. Probando conexión...")
try:
    db = SessionLocal()
    print("   ✓ Sesión creada")
    
    print("\n4. Probando query...")
    from db.models.producto import Producto
    productos = db.query(Producto).all()
    print(f"   ✓ Productos encontrados: {len(productos)}")
    
    if productos:
        print(f"\n5. Primer producto:")
        p = productos[0]
        print(f"   ID: {p.id}")
        print(f"   Nombre: {p.nombre}")
        print(f"   Stock: {p.stock}")
    
    db.close()
    print("\n✅ Todo funciona correctamente!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
