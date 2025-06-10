
# Poster Splitter Web App

Esta aplicación permite subir una imagen y dividirla automáticamente en varias páginas tamaño A4 listas para imprimir como un póster.

## Cómo desplegar en Render

1. Sube el código a un repositorio en GitHub.
2. Entra a [Render](https://render.com).
3. Crea un nuevo Web Service y conecta tu repositorio.
4. Usa esta configuración:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment Variable**: Render asigna automáticamente `PORT`

La app estará accesible en la URL proporcionada por Render.
