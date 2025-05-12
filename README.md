# PROYECTOFINAL

Este proyecto tiene como objetivo ofrecer una plataforma web que permita explorar revistas científicas a través de diferentes filtros como áreas, catálogos y letras iniciales, con funcionalidades de scraping, exploración y gestión de favoritos por usuario.

*Estructura del Proyecto*

Parte 1 - Datos Base
Procesamiento de los archivos CSV con información de revistas y generación de un archivo revistas.json que contiene áreas temáticas y catálogos asociados a cada revista.

Parte 2 - Web Scraper
Script en Python que lee revistas.json y obtiene información adicional de cada revista desde [scimagojr.com]. La información obtenida incluye H-Index, ISSN, publisher, subject area, tipo de publicación, widget e incluso sitio web oficial. Todo esto se guarda en revistas_info.json.

Parte 3 - Plataforma Web
Aplicación web desarrollada con Flask + Bootstrap que permite:

Explorar revistas por letra, área o catálogo

Buscar por nombre

Ver detalles de cada revista

Registrar e iniciar sesión como usuario

Añadir y quitar revistas favoritas (cada usuario tiene su propia lista de favoritos)


*Instrucciones para ejecutar el proyecto*

Estructura de carpetas:

PROYECTOFINAL/
├── parte1/
│   ├── procesar_csv.py
│   └── datos/
│       ├── csv/
│       │   ├── catalogos/
│       │   │   └── *.csv
│       │   ├── areas/
│       │   │   └── *.csv
│       └── json/
│           └── revistas.json
├── parte2/
│   ├── App_Scrapper.py
│   └── datos_scrap/
│       └── revistas_info.json
├── parte3/
│   ├── app.py
│   ├── datos/
│   │   ├── usuarios.json
│   │   └── favoritos.json
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── images/
│   │       └── logo_unison.png
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── revista.html
│       ├── favoritos.html
│       ├── login.html
│       ├── registro.html
│       └── ...otros.html


librerías a instalar:

pip install flask beautifulsoup4 requests unidecode

Paso 1: seguir la estructura de datos mencionada anteriormente 

Paso 2: correr el programa procesar_csv.py para obtener el archivo revistas.json

Paso 3: correr el programa app_scrapper.py para obtener el archivo revistas_info.json

Paso 4:  correr el archivo app.py y dar control + c + click en la URL mostrada en terminal para acceder a la página web resultante

Paso 5: navegar por la web

*Asistente Digital*
Durante el desarrollo de este proyecto se utilizó apoyo de asistentes digitales como ChatGPT y Github Copilot, exclusivamente como herramienta de apoyo para resolver errores, generar estructuras de código y mejorar la lógica de programación, siempre bajo supervisión del equipo.

*Integrantes del equipo*

Francisco Alberto Pinela Alcaraz

Cristian Darey Chavarin Ruiz

Kevin Alejandro Urias Ramirez
