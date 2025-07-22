# Books Scraper – Libros con Rating Alto

Este proyecto realiza web scraping en [Books to Scrape](https://books.toscrape.com/) para obtener una lista de libros con rating alto (4 o 5 estrellas).  
La salida se muestra de forma ordenada en la consola usando la librería [rich](https://github.com/Textualize/rich), y también se exporta a un archivo CSV.

---

## Características
- Scraping de múltiples páginas de libros.
- Filtro automático para ratings de Four y Five.
- Salida en consola estilizada con colores y tabla.
- Indicador de progreso mientras se descargan las páginas.
- Exportación de resultados a CSV.
- Manejo de errores de red con mensajes claros.

---

## Requisitos
- Python 3.8 o superior
- Librerías necesarias:
  ```bash
  pip install requests beautifulsoup4 rich
