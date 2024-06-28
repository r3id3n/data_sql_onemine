# Data SQL OneMine

Esta aplicación permite generar consultas SQL a partir de parámetros seleccionados por el usuario mediante una interfaz gráfica.

## Instalación

1. Clona el repositorio.
2. Navega a la carpeta del proyecto.
3. Crea un entorno virtual:
    ```sh
    python -m venv env
    ```
4. Activa el entorno virtual:
      ```sh
      .\env\Scripts\activate
      ```
5. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el archivo `main.py`:
    ```sh
    python src/main.py
    ```
2. Utiliza la interfaz para seleccionar la consulta deseada, ingresar las fechas, horas y pala.

## Estructura del Proyecto

- `main.py`: Archivo principal que ejecuta la aplicación.
- `sql_queries_xxx.py`: Contiene las consultas SQL.
- `requirements.txt`: Archivo de dependencias.
- `README.md`: Documentación del proyecto.

