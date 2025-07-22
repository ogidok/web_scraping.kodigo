import bs4
import requests
import csv
from rich.console import Console
from rich.table import Table
from rich.progress import track

BASE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'
console = Console()

def get_rating(libro):
    ratings = ['One', 'Two', 'Three', 'Four', 'Five']
    for r in ratings:
        if libro.select(f'.star-rating.{r}'):
            return r
    return None

def scrape_books(paginas=3):
    libros_rating_alto = []
    console.print("[bold cyan]Iniciando scraping de libros...[/bold cyan]\n")
    for pagina in track(range(1, paginas+1), description="Scrapeando páginas"):
        url_pagina = BASE_URL.format(pagina)
        try:
            resultado = requests.get(url_pagina, timeout=10)
            resultado.raise_for_status()
        except requests.RequestException as e:
            console.print(f"[bold red]Error al cargar la página {pagina}: {e}[/bold red]")
            continue

        sopa = bs4.BeautifulSoup(resultado.text, 'lxml')
        libros = sopa.select('.product_pod')
        for libro in libros:
            rating = get_rating(libro)
            if rating in ['Four', 'Five']:
                titulo = libro.select('h3 a')[0]['title']
                precio = libro.select('.price_color')[0].text
                libros_rating_alto.append({
                    'titulo': titulo,
                    'precio': precio,
                    'rating': rating
                })
    return libros_rating_alto

def guardar_csv(libros, filename='libros_rating_alto.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['titulo', 'precio', 'rating'])
        writer.writeheader()
        for libro in libros:
            writer.writerow(libro)

def mostrar_tabla(libros):
    if not libros:
        console.print("[bold yellow]No se encontraron libros con rating alto.[/bold yellow]")
        return
    
    table = Table(title=" Libros con Rating Alto", show_lines=True, style="bright_blue")
    table.add_column("TÍTULO", justify="left", style="cyan", no_wrap=True)
    table.add_column("PRECIO", justify="center", style="green")
    table.add_column("RATING", justify="center", style="magenta")

    for libro in libros:
        table.add_row(libro['titulo'], libro['precio'], libro['rating'])
    
    console.print(table)

if __name__ == '__main__':
    libros = scrape_books(paginas=3)  
    mostrar_tabla(libros)
    guardar_csv(libros)
    console.print(f"\n[bold green]Se guardaron {len(libros)} libros en 'libros_rating_alto.csv'[/bold green]")
