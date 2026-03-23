@echo off
echo 🚀 Preparando subida de KeplerDB Gemini Edition a GitHub...
cd /d "%~dp0"

:: Verificar si el repo ya existe en GitHub
gh repo view KeplerDB_Gemini >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Creando repositorio nuevo en GitHub...
    gh repo create KeplerDB_Gemini --public --source=. --push
) else (
    echo 🔄 El repositorio ya existe. Actualizando...
    git push -u origin master
)

echo.
echo ✅ ¡Todo listo! Tu KeplerDB Gemini Edition ya está en GitHub.
pause
