import os
from Web_Scrapper import cargar_json, guardar_json, buscar_url_revista, extraer_info_revista

# Rutas
RUTA_ENTRADA = os.path.join('..', 'parte1', 'datos', 'json', 'revistas.json')
CARPETA_SALIDA = os.path.join('..', 'parte2', 'datos_scrap')
RUTA_SALIDA = os.path.join(CARPETA_SALIDA, 'revistas_info.json')
RUTA_DESCARTADAS = os.path.join(CARPETA_SALIDA, 'revistas_descartadas.json')

# Crear carpeta si no existe
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Cargar datos
revistas_dict = cargar_json(RUTA_ENTRADA)
datos_existentes = cargar_json(RUTA_SALIDA) if os.path.exists(RUTA_SALIDA) else {}
revistas_descartadas = cargar_json(RUTA_DESCARTADAS) if os.path.exists(RUTA_DESCARTADAS) else {}

# Filtrar solo las revistas que no se han procesado ni descartado
nombres_todas = list(revistas_dict.keys())
nombres_a_procesar = [
    nombre for nombre in nombres_todas
    if nombre not in datos_existentes and nombre not in revistas_descartadas
]

total = len(nombres_a_procesar)
procesadas = 0
fallidas = 0

print(f"🔄 Total de revistas por procesar: {total}")
print(f"📌 Ya procesadas: {len(datos_existentes)}")
print(f"🚫 Ya descartadas: {len(revistas_descartadas)}")
print(f"▶️ Iniciando scraping...\n")

try:
    for i, nombre in enumerate(nombres_a_procesar, start=1):
        print(f"[{i}/{total}] Buscando: {nombre}")
        url = buscar_url_revista(nombre)

        if not url:
            print(f"❌ No se encontró URL para: {nombre}")
            revistas_descartadas[nombre] = "No se encontró URL"
            fallidas += 1
            continue

        print(f"✅ URL encontrada: {url}")
        try:
            datos = extraer_info_revista(url)
            if datos:
                datos_existentes[nombre] = datos
                procesadas += 1
            else:
                revistas_descartadas[nombre] = "No se pudo extraer información"
                fallidas += 1
        except Exception as e:
            print(f"⚠️ Error con {nombre}: {e}")
            revistas_descartadas[nombre] = f"Error: {str(e)}"
            fallidas += 1

        if (procesadas + fallidas) % 5 == 0:
            guardar_json(datos_existentes, RUTA_SALIDA)
            guardar_json(revistas_descartadas, RUTA_DESCARTADAS)
            print(f"💾 Guardado parcial: {procesadas} procesadas, {fallidas} fallidas\n")

except KeyboardInterrupt:
    print("\n🛑 Interrupción detectada. Guardando progreso...")
    guardar_json(datos_existentes, RUTA_SALIDA)
    guardar_json(revistas_descartadas, RUTA_DESCARTADAS)

# Guardado final
guardar_json(datos_existentes, RUTA_SALIDA)
guardar_json(revistas_descartadas, RUTA_DESCARTADAS)
print(f"✅ Scraping completo. {procesadas} procesadas, {fallidas} descartadas.")