REM === Script para generar respaldos de las tablas de datos Maestros ===
REM === del Sistema defcon5.
REM =====================================================================

@echo off
setlocal enabledelayedexpansion

REM Variables para fecha y hora (para log)
for /f "tokens=2-4 delims=/ " %%a in ("%date%") do (
  set YYYY=%%c
  set MM=%%a
  set DD=%%b
)
for /f "tokens=1-2 delims=:." %%a in ("%time%") do (
  set HH=%%a
  set MIN=%%b
)
set TIMESTAMP=%YYYY%-%MM%-%DD%_%HH%-%MIN%

REM Carpeta de destino
set FIXDIR=bcp\fixtures
if not exist "%FIXDIR%" (
  mkdir "%FIXDIR%"
)

REM Archivo log
set LOGFILE=%FIXDIR%\export_log_%TIMESTAMP%.txt
echo Inicio exportacion: %date% %time% > "%LOGFILE%"
echo ---------------------------- >> "%LOGFILE%"

REM Defino arrays "simulados" con variables separadas para modelos y archivos
set MODEL_0=Tipo_Indicador
set MODEL_1=Parametros_G
set MODEL_2=Tipo_Impacto
set MODEL_3=Nivel_Impacto
set MODEL_4=Indicadores_BIA
set MODEL_5=Escenarios
set MODEL_6=Estrategias
set MODEL_7=Tipo_RR
set MODEL_8=Recursos

set FILE_0=tipo_indicador.json
set FILE_1=parametros_g.json
set FILE_2=tipo_impacto.json
set FILE_3=nivel_impacto.json
set FILE_4=indicadores_bia.json
set FILE_5=escenarios.json
set FILE_6=estrategias.json
set FILE_7=tipo_rr.json
set FILE_8=recursos.json

set COUNT=9

REM Loop para exportar cada modelo
for /L %%i in (0,1,%COUNT%) do (
  set MODEL=!MODEL_%%i!
  set FILE=!FILE_%%i!
  echo Exportando !MODEL! a %FIXDIR%\!FILE! ...
  python manage.py dumpdata bcp.!MODEL! --indent 2 > "%FIXDIR%\!FILE!" 2>> "%LOGFILE%"
  if errorlevel 1 (
    echo ❌ Error exportando !MODEL! >> "%LOGFILE%"
    echo ❌ Error exportando !MODEL!
  ) else (
    echo ✅ Exportado !MODEL! >> "%LOGFILE%"
    echo ✅ Exportado !MODEL!
  )
)

echo ---------------------------- >> "%LOGFILE%"
echo Finalizado: %date% %time% >> "%LOGFILE%"

echo.
echo Exportacion terminada. Revisa el log: %LOGFILE%
pause

