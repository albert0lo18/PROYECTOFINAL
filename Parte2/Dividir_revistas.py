import os
import json

# Ruta al archivo original
RUTA_ORIGINAL = os.path.join('..', 'parte1', 'datos', 'json', 'revistas.json')

# Carpeta donde guardar los archivos divididos
CARPETA_SALIDA = os.path.join('..', 'parte1', 'datos', 'json')
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Cargar el archivo original
with open(RUTA_ORIGINAL, 'r', encoding='utf-8') as f:
    revistas = json.load(f)

# Convertir a lista de tuplas (clave, valor) para dividirlo fácilmente
items = list(revistas.items())
total = len(items)
tercio = total // 3

# Dividir en 3 partes
revistas_pinela = dict(items[:tercio])
revistas_chavarin = dict(items[tercio:2*tercio])
revistas_urias = dict(items[2*tercio:])

# Guardar cada archivo
def guardar(nombre_archivo, contenido):
    path = os.path.join(CARPETA_SALIDA, nombre_archivo)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(contenido, f, indent=2, ensure_ascii=False)
    print(f"✅ Guardado: {nombre_archivo} ({len(contenido)} revistas)")

guardar('revistas_pinela.json', revistas_pinela)
guardar('revistas_chavarin.json', revistas_chavarin)
guardar('revistas_urias.json', revistas_urias)

