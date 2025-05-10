from flask import Flask, render_template, request, jsonify
import json
from collections import defaultdict

app = Flask(__name__)

# Cargar datos de revistas
with open('datos/revistas_info.json', 'r', encoding='utf-8') as f:
    revistas_data = json.load(f)

# Preprocesar datos para búsquedas más eficientes
def preprocess_data():
    areas = defaultdict(list)
    catalogos = defaultdict(list)
    letras = defaultdict(list)
    
    # Generar todas las letras del abecedario primero
    abecedario = [chr(i) for i in range(65, 91)]  # A-Z
    
    for titulo, datos in revistas_data.items():
        # Validar datos esenciales
        if not titulo or not isinstance(titulo, str):
            continue
            
        publisher = datos.get('publisher')
        if not publisher or not isinstance(publisher, str):
            continue
            
        h_index = datos.get('h_index', '0')
        subject_areas = datos.get('subject_area', [])
        
        # Procesar áreas
        for area in subject_areas:
            if area and isinstance(area, str):
                areas[area].append({
                    'titulo': titulo,
                    'h_index': h_index
                })
        
        # Procesar catálogos
        catalogos[publisher].append({
            'titulo': titulo,
            'h_index': h_index
        })
        
        # Procesar letras iniciales
        if titulo:  # Asegurarse que el título no esté vacío
            letra_inicial = titulo[0].upper()
            if letra_inicial in abecedario:  # Solo si es una letra A-Z
                letras[letra_inicial].append({
                    'titulo': titulo,
                    'h_index': h_index,
                    'areas': subject_areas,
                    'catalogos': [publisher]
                })
    
    # Asegurarnos de que todas las letras existan, aunque estén vacías
    for letra in abecedario:
        if letra not in letras:
            letras[letra] = []
    
    return areas, catalogos, letras

areas_data, catalogos_data, letras_data = preprocess_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/areas')
def areas():
    areas_list = sorted(areas_data.keys())
    return render_template('areas.html', areas=areas_list)

@app.route('/area/<area_name>')
def area_detail(area_name):
    revistas = areas_data.get(area_name, [])
    return render_template('area_detail.html', area_name=area_name, revistas=revistas)

@app.route('/catalogos')
def catalogos():
    catalogos_list = sorted([k for k in catalogos_data.keys() if k is not None])
    return render_template('catalogos.html', catalogos=catalogos_list)

@app.route('/catalogo/<catalogo_name>')
def catalogo_detail(catalogo_name):
    revistas = catalogos_data.get(catalogo_name, [])
    return render_template('catalogo_detail.html', catalogo_name=catalogo_name, revistas=revistas)

@app.route('/explorar')
def explorar():
    letras = sorted(letras_data.keys())
    return render_template('explorar.html', letras=letras)

@app.route('/explorar/<letra>')
def explorar_letra(letra):
    # Validar que la letra sea una sola letra mayúscula A-Z
    if len(letra) != 1 or not letra.isalpha() or not letra.isupper():
        return "Letra no válida", 400
        
    revistas = letras_data.get(letra, [])
    return render_template('explorar_letra.html', letra=letra, revistas=revistas)

@app.route('/busqueda')
def busqueda():
    query = request.args.get('q', '')
    resultados = []
    
    if query:
        query = query.lower()
        for titulo, datos in revistas_data.items():
            if query in titulo.lower():
                resultados.append({
                    'titulo': titulo,
                    'h_index': datos['h_index'],
                    'areas': datos['subject_area'],
                    'catalogos': [datos['publisher']]
                })
    
    return render_template('busqueda.html', resultados=resultados, query=query)

@app.route('/revista/<titulo>')
def revista(titulo):
    revista = revistas_data.get(titulo)
    if not revista:
        return "Revista no encontrada", 404
    return render_template('revista.html', revista=revista, titulo=titulo)

@app.route('/creditos')
def creditos():
    desarrolladores = [
        {'nombre': 'Cristian Darey Chavarin Ruiz', 'foto': 'foto1.jpg'},
        {'nombre': 'Francisco Alberto Pinela Alcaraz', 'foto': 'foto2.jpg'},
        {'nombre': 'Kevin Alejandro Urias Ramirez', 'foto': 'foto3.jpg'}
    ]
    return render_template('creditos.html', desarrolladores=desarrolladores)

if __name__ == '__main__':
    app.run(debug=True)