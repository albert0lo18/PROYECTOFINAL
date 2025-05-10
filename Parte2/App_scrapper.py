import os
import time
from Web_Scrapper import cargar_json, guardar_json, buscar_url_revista, extraer_info_revista

# Rutas
RUTA_ENTRADA = os.path.join('..', 'parte1', 'datos', 'json', 'revistas.json')
CARPETA_SALIDA = os.path.join('..', 'parte2', 'datos_scrap')
RUTA_SALIDA = os.path.join(CARPETA_SALIDA, 'revistas_info.json')

# Crear carpeta si no existe
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Cargar datos
revistas = cargar_json(RUTA_ENTRADA)
datos_existentes = cargar_json(RUTA_SALIDA) if os.path.exists(RUTA_SALIDA) else {}

procesadas = 0
limite = 50  # cambia si quieres

try:
    for nombre in revistas:
        if nombre in datos_existentes:
            continue

        print(f"🔍 Buscando: {nombre}")
        url = buscar_url_revista(nombre)

        if not url:
            print(f"❌ No se encontró URL para: {nombre}")
            continue

        print(f"✅ URL encontrada: {url}")
        try:
            datos = extraer_info_revista(url)
            if datos:  # solo guarda si hay datos válidos
                datos_existentes[nombre] = datos
                procesadas += 1
        except Exception as e:
            print(f"⚠️ Error con {nombre}: {e}")

        if procesadas % 5 == 0:
            guardar_json(datos_existentes, RUTA_SALIDA)
            print("💾 Guardado parcial...")


except KeyboardInterrupt:
    print("\n🛑 Interrupción detectada. Guardando lo procesado...")
    guardar_json(datos_existentes, RUTA_SALIDA)

# Guardado final
guardar_json(datos_existentes, RUTA_SALIDA)
print("✅ Scraping completo.")
