# 🧑‍🔧 Sistema Taller de Diego

Proyecto de sistema desarrollado con **FastAPI**.

---

## 📌 Funcionalidades principales

- Registro e historial de servicios
- Listado, actualización y eliminación de productos.
- Gestión y asignación de empleados.

---

## 🚀 Tecnologías

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic v2
- SQLite

### Frontend
- HTML 5
- CSS 3
- JavaScript
- TailwindCSS

---

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/ESIS-DevTeam/Taller-Diego.git
cd Taller-Diego
```
2. Crea y activa un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # Linux/Mac
```
4. Instala las dependencias:
```bash
pip install -r requirements.txt
```
5. Cambia el path de python a backend
```bash
$env:PYTHONPATH = "backend"
```
6. Crea el archivo `.env` en la carpeta `backend` con la conexión a Supabase
```env
DATABASE_URL="<link>"
SUPABASE_URL="<link>"
SUPABASE_ANON_KEY="<ANON PUBLIC KEY>>"
JWT_SECRET="<SECRET KEY ES256>"
```
7. Ejecuta el script para crear las tablas
```bash
python .\backend\database.py
```
8. Corre el servidor:
```bash
uvicorn main:app --reload
```
### 🗂️ Estructura del proyecto

```plaintext
app/
├── backend/
│   ├── api/                  # Rutas FastAPI organizadas por versión
│   │   └── v1/
│   │       └── routes/
│   │           └── producto_routes.py
│   │
│   ├── core/                 # Configuración central (env, settings, etc.)
│   │   └── config.py
│   │
│   ├── db/                   # Conexión y modelos de base de datos
│   │   ├── base.py
│   │   └── models/
│   │       └── producto.py
│   │
│   ├── schemas/              # Esquemas Pydantic (validación y serialización)
│   │   └── producto_schema.py
│   │
│   ├── repositories/         # Repositorios: acceso y persistencia de datos
│   │   └── producto_repo.py
│   │
│   └── services/             # Servicios: lógica de negocio
│       └── producto_service.py
│
├── frontend/
│   ├── assets/               # Recursos, imagenes, iconos, fuentes
│   ├── views/                # Archivos HTML o plantillas
│   │   └── index.html        # Archivo de ejemplo principal
│   ├── styles/               # Archivos CSS
│   └── scripts/              # Archivos JavaScript
│
├── main.py                   # Punto de entrada principal de la app
├── requirements.txt          # Dependencias de Python
└── README.md                 # Documentación del proyecto
```