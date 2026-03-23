@echo off
setlocal
echo 🚀 Sincronizando cambios con GitHub y Hugging Face...
cd /d "%~dp0"

:: Pedir mensaje de commit
set /p msg="Introduce el mensaje del cambio (Enter para usar 'Mejoras generales'): "
if "%msg%"=="" set msg=Mejoras generales

:: 1. Añadir y hacer commit local
echo 📝 Guardando cambios locales...
git add .
git commit -m "%msg%"

:: 2. Subir a GitHub (origin)
echo 📦 Subiendo a GitHub...
git push origin main

:: 3. Subir a Hugging Face (hf)
echo ☁️ Desplegando en Hugging Face...
git push hf main

echo.
echo ✅ ¡Todo sincronizado!
echo 🔗 GitHub: https://github.com/Eduxx76/KeplerDB_Gemini
echo 🔗 App: https://huggingface.co/spaces/Eduxx76/KeplerDB_Gemini
echo.
pause
