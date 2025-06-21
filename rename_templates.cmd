@echo off
echo ==== Renombrando carpeta BCP a bcp de forma segura ====

cd /d "%~dp0"

REM Paso 1: renombrar temporalmente
git mv bcp\templates\BCP bcp\templates\temp_bcp

REM Paso 2: renombrar a nombre final en minúsculas
git mv bcp\templates\temp_bcp bcp\templates\bcp

REM Paso 3: confirmar cambios
git status

echo.
echo === Cambios listos para confirmar. Ahora ejecuta:
echo     git commit -m "Renombrado carpeta BCP a bcp en templates para compatibilidad Render"
echo     git push
echo.
pause
