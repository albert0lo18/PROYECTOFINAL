import os
from Web_Scrapper import cargar_json, guardar_json, buscar_url_revista, extraer_info_revista

# Rutas
RUTA_ENTRADA = os.path.join('..', 'parte1', 'datos', 'json', 'revistas.json')
CARPETA_SALIDA = os.path.join('..', 'parte2', 'datos_scrap')
RUTA_SALIDA = os.path.join(CARPETA_SALIDA, 'revistas_info.json')

# Crear carpeta si no existe
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Cargar datos
revistas_dict = cargar_json(RUTA_ENTRADA)
datos_existentes = cargar_json(RUTA_SALIDA) if os.path.exists(RUTA_SALIDA) else {}

# Filtrar solo las revistas que no se han procesado aún
nombres_todas = list(revistas_dict.keys())
nombres_a_procesar = [nombre for nombre in nombres_todas if nombre not in datos_existentes]

total = len(nombres_a_procesar)
procesadas = 0

print(f"🔄 Total de revistas por procesar: {total}")
print(f"📌 Ya procesadas anteriormente: {len(datos_existentes)}")
print(f"▶️ Iniciando scraping...\n")

try:
    for i, nombre in enumerate(nombres_a_procesar, start=1):
        print(f"[{i}/{total}] Buscando: {nombre}")
        url = buscar_url_revista(nombre)

        if not url:
            print(f"❌ No se encontró URL para: {nombre}")
            continue

        print(f"✅ URL encontrada: {url}")
        try:
            datos = extraer_info_revista(url)
            if datos:
                datos_existentes[nombre] = datos
                procesadas += 1
        except Exception as e:
            print(f"⚠️ Error con {nombre}: {e}")

        if procesadas % 5 == 0:
            guardar_json(datos_existentes, RUTA_SALIDA)
            print(f"💾 Guardado parcial... Total nuevas procesadas: {procesadas}\n")

except KeyboardInterrupt:
    print("\n🛑 Interrupción detectada. Guardando progreso...")
    guardar_json(datos_existentes, RUTA_SALIDA)

# Guardado final
guardar_json(datos_existentes, RUTA_SALIDA)
print(f"✅ Scraping completo. Se procesaron {procesadas} nuevas revistas.")
