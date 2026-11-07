## 🛠️ Fase 1: Paso 1 - Configuración Detallada del Entorno (Desde Cero)

### 1\. Control de Versiones de Python y Creación del Entorno con Python 3.11.9

En tu sistema operativo puedes tener varias versiones de Python instaladas. Para asegurarnos de que este proyecto corra específicamente sobre **Python 3.11.9** (aislado de la versión global de tu PC), utilizaremos el comando explícito apuntando a esa versión.

Abre tu terminal (PowerShell o CMD) dentro de la carpeta de tu nuevo proyecto (`backend-premium-api-2`) y ejecuta:

```bash
# Indicar explícitamente que queremos usar Python 3.11.9 para crear el entorno virtual
py -3.11 -m venv .venv
# O alternativamente si usas el ejecutable directo:
# python3.11 -m venv .venv

```

> \\\*\\\*💡 Tip Senior / Inglés Técnico:\\\*\\\* Especificar versiones exactas de runtime (como `Python 3.11.9`) garantiza la \\\*reproducibilidad\\\* del entorno y evita bugs inesperados por incompatibilidades de sintaxis o librerías nativas (\\\*dependency conflicts\\\*).

\---

### 2\. Permicios de Ejecución en Windows 11 (PowerShell Execution Policy)

Si intentas activar el entorno virtual en PowerShell y te arroja un error rojo diciendo que *los scripts están deshabilitados en este sistema*, se debe a la directiva de seguridad por defecto de Windows 11.

Para solucionarlo de forma segura en tu usuario actual, ejecuta en tu terminal de PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

* **¿Qué hace esto?** Permite que tu terminal ejecute scripts locales (como el archivo `activate.ps1` de tu entorno virtual) sin comprometer la seguridad global del equipo.

Ahora sí, procede a activar tu entorno virtual:

```powershell
.venv\\\\Scripts\\\\activate

```

*(Verás que la terminal ahora muestra `(.venv)` a la izquierda, confirmando que estás dentro del entorno aislado).*

\---

### 3\. Verificación de Python y Actualización de Herramientas Base

Estando con el entorno virtual activo, corrobora que estás usando la versión correcta y actualiza el gestor de paquetes (`pip`):

```bash
# Verificar la versión exacta de Python activa en el entorno
python --version
# Debería retornar: Python 3.11.9

# Actualizar pip a la última versión disponible
python -m pip install --upgrade pip

```

\---

### 4\. Configuración de PostgreSQL en Docker

Para mantener limpio tu sistema operativo, usaremos Docker Desktop para correr nuestra base de datos.

Asegúrate de que Docker esté abierto y ejecuta el siguiente comando para descargar y levantar el contenedor de PostgreSQL 15:

```bash
docker run --name postgres-db -e POSTGRES\\\_USER=postgres -e POSTGRES\\\_PASSWORD=postgres -e POSTGRES\\\_DB=backend\\\_db -p 5432:5432 -d postgres:15

```

Para verificar que el motor de base de datos está corriendo saludablemente:

```bash
docker ps

```

\---

### 5\. Creación del Archivo `requirements.txt` y Variables de Entorno (`.env`)

Crea los dos archivos clave en la raíz de tu proyecto:

**`requirements.txt`**

```text
fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.6.4
pydantic-settings>=2.2.1
sqlalchemy>=2.0.27
psycopg2-binary>=2.9.9
alembic>=1.13.1
passlib\\\[bcrypt]>=1.7.4
python-multipart>=0.0.9
python-jose\\\[cryptography]>=3.3.0
pytest>=8.0.0
httpx>=0.26.0
pytest-cov>=4.1.0

```

**`.env`**

```env
PROJECT\\\_NAME="Premium Backend API"
DATABASE\\\_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/backend\\\_db"
SECRET\\\_KEY="tu\\\_super\\\_secret\\\_key\\\_ultrasecured\\\_change\\\_it\\\_in\\\_production"
ALGORITHM="HS256"
ACCESS\\\_TOKEN\\\_EXPIRE\\\_MINUTES=30

```

Instala las dependencias dentro de tu entorno virtual:

```bash
pip install -r requirements.txt

```

\---

### 📂 Estructura de Carpetas Limpia

Construye manualmente la estructura inicial de directorios en tu proyecto:

```text
backend-premium-api-2/
├── app/
│   ├── api/
│   │   ├── \\\_\\\_init\\\_\\\_.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── \\\_\\\_init\\\_\\\_.py
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── \\\_\\\_init\\\_\\\_.py
│   │           ├── auth.py
│   │           ├── users.py
│   │           └── items.py
│   ├── core/
│   │   ├── \\\_\\\_init\\\_\\\_.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── \\\_\\\_init\\\_\\\_.py
│   │   ├── base.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── \\\_\\\_init\\\_\\\_.py
│   │   ├── token.py
│   │   ├── user.py
│   │   └── item.py
│   └── tests/
│       ├── \\\_\\\_init\\\_\\\_.py
│       ├── conftest.py
│       └── test\\\_users.py
├── .env
├── requirements.txt
└── README.md

```

\---

### ¿Cómo seguimos?

Tómate el tiempo necesario para replicar esto en tu carpeta `backend-premium-api-2`, verificar que todo levante bien y que el entorno apunte a Python 3.11.9.

**Por favor, avísame cuando hayas completado y validado este Paso 1 en tu máquina para que avancemos juntos al Paso 2** (la creación del núcleo de configuración y conexión a la base de datos).

