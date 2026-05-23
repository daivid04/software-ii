"""
Script para insertar datos de ejemplo de productos en la base de datos.

Ejecutar con: python .\backend\seed_productos.py
"""

from db.base import SessionLocal, engine, Base
from db.models.producto import Producto

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Datos de ejemplo de productos para taller
productos_ejemplo = [
    {
        "nombre": "Aceite 10W-40",
        "descripcion": "Aceite mineral 10W-40 para motores de gasolina",
        "precio_venta": 25000,
        "precio_compra": 15000,
        "marca": "Shell",
        "categoria": "Aceites",
        "stock": 50,
        "stock_minimo": 10,
        "tipo": "producto"
    },
    {
        "nombre": "Filtro de Aire",
        "descripcion": "Filtro de aire para motores gasolina",
        "precio_venta": 18000,
        "precio_compra": 10000,
        "marca": "Fram",
        "categoria": "Filtros",
        "stock": 30,
        "stock_minimo": 5,
        "tipo": "producto"
    },
    {
        "nombre": "Filtro de Aceite",
        "descripcion": "Filtro de aceite universal",
        "precio_venta": 12000,
        "precio_compra": 7000,
        "marca": "Fram",
        "categoria": "Filtros",
        "stock": 40,
        "stock_minimo": 8,
        "tipo": "producto"
    },
    {
        "nombre": "Pastillas de Freno",
        "descripcion": "Juego de pastillas de freno delanteras",
        "precio_venta": 85000,
        "precio_compra": 50000,
        "marca": "Brembo",
        "categoria": "Sistema de Frenos",
        "stock": 15,
        "stock_minimo": 3,
        "tipo": "producto"
    },
    {
        "nombre": "Bujías",
        "descripcion": "Bujía de encendido estándar",
        "precio_venta": 15000,
        "precio_compra": 8000,
        "marca": "NGK",
        "categoria": "Encendido",
        "stock": 60,
        "stock_minimo": 15,
        "tipo": "producto"
    },
    {
        "nombre": "Correa de Distribución",
        "descripcion": "Caorrea de distribución originl",
        "precio_venta": 120000,
        "precio_compra": 70000,
        "marca": "Continental",
        "categoria": "Motor",
        "stock": 8,
        "stock_minimo": 2,
        "tipo": "producto"
    },
    {
        "nombre": "Batería 12V 60Ah",
        "descripcion": "Batería para vehículos gasolina",
        "precio_venta": 180000,
        "precio_compra": 100000,
        "marca": "Bosch",
        "categoria": "Eléctrico",
        "stock": 10,
        "stock_minimo": 2,
        "tipo": "producto"
    },
    {
        "nombre": "Líquido de Frenos",
        "descripcion": "Líquido de frenos DOT 4",
        "precio_venta": 22000,
        "precio_compra": 12000,
        "marca": "Castrol",
        "categoria": "Fluidos",
        "stock": 25,
        "stock_minimo": 5,
        "tipo": "producto"
    },
    {
        "nombre": "Anticongelante",
        "descripcion": "Anticongelante concentrado rojo",
        "precio_venta": 35000,
        "precio_compra": 18000,
        "marca": "Prestone",
        "categoria": "Fluidos",
        "stock": 20,
        "stock_minimo": 4,
        "tipo": "producto"
    },
    {
        "nombre": "Amortiguador Delantero",
        "descripcion": "Amortiguador delantero derecho/izquierdo",
        "precio_venta": 95000,
        "precio_compra": 55000,
        "marca": "KYB",
        "categoria": "Suspensión",
        "stock": 12,
        "stock_minimo": 2,
        "tipo": "producto"
    }
]

def seed_productos():
    """Inserta productos de ejemplo en la base de datos."""
    db = SessionLocal()
    
    try:
        # Verificar si ya existen productos
        existing_count = db.query(Producto).count()
        if existing_count > 0:
            print(f"Ya existen {existing_count} productos en la base de datos.")
            respuesta = input("¿Desea eliminarlos y crear nuevos? (s/n): ")
            if respuesta.lower() == 's':
                db.query(Producto).delete()
                db.commit()
                print("Productos eliminados.")
            else:
                print("Operación cancelada.")
                return
        
        # Insertar productos
        for producto_data in productos_ejemplo:
            producto = Producto(**producto_data)
            db.add(producto)
        
        db.commit()
        print(f"✅ {len(productos_ejemplo)} productos insertados exitosamente!")
        
        # Mostrar productos creados
        print("\nProductos creados:")
        for producto in db.query(Producto).all():
            print(f"  - {producto.id}: {producto.nombre} | Stock: {producto.stock} | ${producto.precio_venta}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_productos()
