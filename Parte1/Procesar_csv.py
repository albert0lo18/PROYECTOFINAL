import os
import json

RUTA_DATOS = 'datos'
RUTA_CSV = os.path.join(RUTA_DATOS, 'csv')
RUTA_AREAS = os.path.join(RUTA_CSV, 'areas')
RUTA_CATALOGOS = os.path.join(RUTA_CSV, 'catalogos')
RUTA_JSON = os.path.join(RUTA_DATOS, 'json', 'revistas.json')

def extraer_nombres_revista(ruta_archivo):
    """
    Lee el archivo CSV y devuelve un conjunto de nombres de revista y catálogos.
    Maneja el caso especial de ED_INST.csv.
    """
    nombres_revista = []
    codificaciones_a_probar = ['utf-8', 'latin-1', 'cp1252', 'ISO-8859-1']

    for codificacion in codificaciones_a_probar:
        try:
            with open(ruta_archivo, 'r', encoding=codificacion) as archivo_csv:
                if os.path.basename(ruta_archivo) == 'ED_INST.csv':
                    next(archivo_csv)  # Saltar la primera línea
                    for linea in archivo_csv:
                        partes = linea.strip().split(',')
                        if len(partes) == 2:
                            nombre = partes[0].upper()
                            catalogo = partes[1].upper()
                            if nombre:
                                nombres_revista.append({'nombre': nombre, 'catalogo': catalogo})
                        elif linea.strip():
                            print(f"Advertencia: Línea inesperada en {ruta_archivo}: {linea.strip()}")
                else:
                    for linea in archivo_csv:
                        nombre = linea.strip().upper()
                        if nombre:
                            nombres_revista.append({'nombre': nombre, 'catalogo': None})  # Catálogo None para otros archivos
                return nombres_revista
        except UnicodeDecodeError:
            print(f"Error de decodificación con {codificacion} en {ruta_archivo}. Probando otra codificación...")
            pass
        except Exception as e:
            print(f"Error no relacionado con la codificación al leer {ruta_archivo}: {e}")
            return []

    print(f"No se pudo leer {ruta_archivo} con ninguna de las codificaciones probadas.")
    return []


def generar_diccionario_revistas():
    """
    Genera el diccionario de revistas.
    """
    diccionario = {}

    # Procesar archivos de áreas
    if os.path.exists(RUTA_AREAS):
        for nombre_archivo in os.listdir(RUTA_AREAS):
            if nombre_archivo.endswith('.csv'):
                ruta_completa = os.path.join(RUTA_AREAS, nombre_archivo)
                revistas_encontradas = extraer_nombres_revista(ruta_completa)
                nombre_archivo_sin_csv = nombre_archivo.replace('.csv', '').upper()
                for revista_info in revistas_encontradas:
                    revista = revista_info['nombre']
                    catalogo_revista = revista_info['catalogo']
                    if revista not in diccionario:
                        diccionario[revista] = {'areas': [], 'catalogos': []}
                    if nombre_archivo_sin_csv not in diccionario[revista]['areas']:
                        diccionario[revista]['areas'].append(nombre_archivo_sin_csv)
                    if catalogo_revista: #solo añade si no es None
                         if catalogo_revista not in diccionario[revista]['catalogos']:
                            diccionario[revista]['catalogos'].append(catalogo_revista)

    # Procesar archivos de catálogos
    if os.path.exists(RUTA_CATALOGOS):
        for nombre_archivo in os.listdir(RUTA_CATALOGOS):
            if nombre_archivo.endswith('.csv'):
                ruta_completa = os.path.join(RUTA_CATALOGOS, nombre_archivo)
                revistas_encontradas = extraer_nombres_revista(ruta_completa)
                nombre_archivo_sin_csv = nombre_archivo.replace('.csv', '').upper()
                for revista_info in revistas_encontradas:
                    revista = revista_info['nombre']
                    catalogo_revista = revista_info['catalogo']
                    if revista not in diccionario:
                        diccionario[revista] = {'areas': [], 'catalogos': []}
                    if nombre_archivo_sin_csv not in diccionario[revista]['catalogos']:
                        diccionario[revista]['catalogos'].append(nombre_archivo_sin_csv)
                    if catalogo_revista: #solo añade si no es None
                        if catalogo_revista not in diccionario[revista]['catalogos']:
                            diccionario[revista]['catalogos'].append(catalogo_revista)

    return diccionario

def guardar_json(diccionario, ruta_archivo):
    """
    Guarda el diccionario en un archivo JSON.
    """
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, 'w') as archivo_json:
        json.dump(diccionario, archivo_json, indent=4)

def leer_json(ruta_archivo):
    """
    Lee el diccionario desde un archivo JSON e imprime su contenido.
    """
    try:
        with open(ruta_archivo, 'r') as archivo_json:
            diccionario_leido = json.load(archivo_json)
        print("\nContenido del archivo JSON:")
        print(json.dumps(diccionario_leido, indent=4, ensure_ascii=False))  
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")

if __name__ == "__main__":
    diccionario_final = generar_diccionario_revistas()
    guardar_json(diccionario_final, RUTA_JSON)
    print(f"Archivo JSON guardado en: {RUTA_JSON}")
    leer_json(RUTA_JSON)
