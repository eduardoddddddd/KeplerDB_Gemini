# Propuestas de Codex

Trabajo desde Codex (el modelo LLM que me representa) y, tras leer README.md, veo tres áreas clave para consolidar y mejorar KeplerDB:

## 1. Documentación complementaria
- **Instalación clara:** detallar pip install -r requirements.txt o, si el proyecto no tiene equirements.txt, listar los paquetes (Flask, pyswisseph, matplotlib) y sugerir py -m pip install --upgrade pip setuptools antes.
- **Cómo regenerar kepler.db:** explicar qué scripts (uild_kepler_db.py, inject_tab_kepler.py) se usan, qué archivos fuente (*.ASC) necesita, y si hay pasos para actualizar la tabla de cartas históricas.
- **Guía de endpoints:** añadir ejemplos concretos con curl o fetch sobre /calcular, /transitos, /sinastria; incluir payload mínimo y mostrar qué devuelve (JSON + HTML + base64 imagen).
- **Pruebas manuales:** una sección con pasos para verificar que los tabs, las búsquedas y la exportación PDF funcionan (por ejemplo, usar la UI para generar una carta y un informe PDF). También indicar cómo reiniciar Flask si se cambia kepler_interp.py (ej. importlib.reload ya mencionado).

## 2. UX y operativa
- **Endpoints adicionales:** proponer /estado para saber si la base de datos y el importador de cartas guardadas están disponibles.
- **Datos de prueba:** incluir ejemplos de cartas guardadas y una pequeña muestra de la colección histórica para poder probar sin cargar 8502 registros.
- **Mejorar la pestaña de famosos:** explicar qué filtros están disponibles, cómo se comportan los debounce y qué campos se pueden insertar en la búsqueda para replicar resultados desde el README.

## 3. Roadmap y mantenimiento
- **Checklist de despliegue:** pasos concretos para  subir a Render o Railway (crear .env, usar gunicorn, establecer rutas relativas, etc.).
- **Backups y regeneración:** cómo respaldar %USERPROFILE%\astro_cartas y qué hacer si se corrompe kepler.db (recrear con uild_kepler_db.py).
- **Pruebas de regresión:** sugerir agregar un pequeño script de smoke test que verifique /calcular y /sinastria, idealmente integrable en CI.

## 4. Planificación para portabilidad
- Definir un pyproject.toml/setup.cfg (o setup.py si hace falta) que liste las dependencias fijas (Flask, pyswisseph, matplotlib, etc.) y declare los datos (kepler.db, los archivos .ASC, ejemplos de cartas) como package_data o data_files.
- Añadir un entry point CLI (por ejemplo keplerdb=kepler_interp:main) para arrancar el servidor/los endpoints con un solo keplerdb --serve después de pip install . o similar.
- Centralizar la lectura del kepler.db en un helper que use importlib.resources/pkgutil.get_data, con la opción KEPLERDB_PATH para sobrescribir la ubicación (por ejemplo, para usar una copia en %USERPROFILE%\astro_cartas).
- Especificar un flujo reproducible para regenerar la base: script scripts/prepare_db.py + datos .ASC, y registrar los pasos en la doc para recomponer la DB si se descompone.
- Crear plantillas para instalación rápida: Makefile/	asks.py/setup.ps1 que creen un virtualenv/venv, instalen dependencias y lancen el servidor con la URL http://localhost:5000.
- Evaluar contenedores (Docker python:3.12-slim) o zipapp/pipx para facilitar la distribución si se decide salir del entorno local.
- Anotar estos pasos en el README o Codex_proposals.md (como se ha hecho aquí) y definir qué se hará primero para avanzar con la portabilidad.

¿Te gustaría que convierta estas propuestas en issues o actualice el README con una de estas secciones?
