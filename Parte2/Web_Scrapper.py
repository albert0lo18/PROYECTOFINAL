import os, json, time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from unidecode import unidecode


HEADERS = {'User-Agent': 'Mozilla/5.0'}

BASE_URL = "https://www.scimagojr.com/journalsearch.php?q="

def cargar_json(path):
    with open(path, 'r', encoding='latin-1') as f:
        return json.load(f)

def guardar_json(data, path):
    with open(path, 'w', encoding='latin-1') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def buscar_url_revista(nombre_revista):
    url = BASE_URL + quote(nombre_revista)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    for a in soup.select('div.search_results a'):
        span = a.find('span', class_='jrnlname')
        if span:
            nombre_span = unidecode(span.text.strip().lower())
            nombre_buscado = unidecode(nombre_revista.strip().lower())
            if nombre_buscado in nombre_span:
                return "https://www.scimagojr.com/" + a['href']
    return None

def extraer_info_revista(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    def extraer_por_titulo(titulo):
        bloques = soup.find_all('div')
        for bloque in bloques:
            encabezado = bloque.find('h2')
            if encabezado and encabezado.text.strip() == titulo:
                parrafo = bloque.find('p')
                if parrafo:
                    return parrafo.get_text(strip=True)
        return None

    def extraer_subject_area():
        contenedor = soup.find('h2', string="Subject Area and Category")
        if contenedor:
            bloque = contenedor.find_parent('div')
            if bloque:
                return [li.get_text(strip=True) for li in bloque.select('ul.treecategory li')]
        return []

    def extraer_hindex():
        h_tags = soup.select("p.hindexnumber")
        return h_tags[1].text.strip() if len(h_tags) > 1 else None

    def extraer_widget():
        input_tag = soup.select_one('#embed_code')
        return input_tag['value'] if input_tag else None

    return {
        "sitio_web": url,
        "h_index": extraer_hindex(),
        "subject_area": extraer_subject_area(),
        "publisher": extraer_por_titulo("Publisher"),
        "issn": extraer_por_titulo("ISSN"),
        "widget": extraer_widget(),
        "publication_type": extraer_por_titulo("Publication type")
    }
