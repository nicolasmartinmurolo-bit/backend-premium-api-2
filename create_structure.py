import os
from pathlib import Path

# Definimos la lista de directorios y archivos que componen nuestra arquitectura limpia
# Clean Layered Architecture structure definition
STRUCTURE = [
    "app/__init__.py",
    "app/api/__init__.py",
    "app/api/deps.py",
    "app/api/v1/__init__.py",
    "app/api/v1/api.py",
    "app/api/v1/endpoints/__init__.py",
    "app/api/v1/endpoints/auth.py",
    "app/api/v1/endpoints/users.py",
    "app/api/v1/endpoints/items.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/database.py",
    "app/core/security.py",
    "app/models/__init__.py",
    "app/models/base.py",
    "app/models/user.py",
    "app/models/item.py",
    "app/schemas/__init__.py",
    "app/schemas/token.py",
    "app/schemas/user.py",
    "app/schemas/item.py",
    "app/tests/__init__.py",
    "app/tests/conftest.py",
    "app/tests/test_users.py",
    ".env",
    "requirements.txt",
    "README.md"
]

def create_project_structure():
    print("🚀 Iniciando la creación automática de la estructura del proyecto...")
    
    for file_path_str in STRUCTURE:
        file_path = Path(file_path_str)
        
        # Crear los directorios padres si no existen
        if file_path.parent != Path(""):
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
        # Crear el archivo si no existe (vacío)
        if not file_path.exists():
            file_path.touch()
            print(f"📄 Creado: {file_path}")
        else:
            print(f"⚠️ Ya existe (omitido): {file_path}")
            
    print("\n✅ ¡Estructura de directorios y archivos generada exitosamente!")

if __name__ == "__main__":
    create_project_structure()