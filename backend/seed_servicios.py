"""
Script para insertar datos de ejemplo de servicios en la base de datos.

Ejecutar con: python -m backend.seed_servicios
"""

from db.base import SessionLocal, engine, Base
from db.models.servicio import Servicio

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Datos de ejemplo
servicios_ejemplo = [
    {
        "nombre": "Cambio de Aceite",
        "descripcion": "Cambio de aceite y filtro"
    },
    {
        "nombre": "Alineación y Balanceo",
        "descripcion": "Alineación y balanceo de ruedas"
    },
    {
        "nombre": "Revisión de Frenos",
        "descripcion": "Revisión completa del sistema de frenos"
    },
    {
        "nombre": "Diagnóstico Computarizado",
        "descripcion": "Escaneo computarizado del vehículo"
    },
    {
        "nombre": "Cambio de Bujías",
        "descripcion": "Cambio de bujías y revisión de sistema de encendido"
    }
]

def seed_servicios():
    """Inserta servicios de ejemplo en la base de datos."""
    db = SessionLocal()
    
    try:
        # Verificar si ya existen servicios
        existing_count = db.query(Servicio).count()
        if existing_count > 0:
            print(f"Ya existen {existing_count} servicios en la base de datos.")
            respuesta = input("¿Desea eliminarlos y crear nuevos? (s/n): ")
            if respuesta.lower() == 's':
                db.query(Servicio).delete()
                db.commit()
                print("Servicios eliminados.")
            else:
                print("Operación cancelada.")
                return
        
        # Insertar servicios
        for servicio_data in servicios_ejemplo:
            servicio = Servicio(**servicio_data)
            db.add(servicio)
        
        db.commit()
        print(f"✅ {len(servicios_ejemplo)} servicios insertados exitosamente!")
        
        # Mostrar servicios creados
        print("\nServicios creados:")
        for servicio in db.query(Servicio).all():
            print(f"  - {servicio.id}: {servicio.nombre}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_servicios()
