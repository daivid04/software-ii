from db.base import engine, Base
import backend.db

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente en Supabase")
