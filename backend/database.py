from db.base import engine, Base
import db.models

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente en Supabase")
