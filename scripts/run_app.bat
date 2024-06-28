@echo off
REM Cambiar a la carpeta del proyecto
cd /d C:\Users\Felipe Valencia\Documents\Onemine\data_sql_onemine

REM Activar el entorno virtual
call env\Scripts\activate

REM Ejecutar el script Python
python src\main.py

REM Desactivar el entorno virtual (opcional)
deactivate
