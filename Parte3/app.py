from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from collections import defaultdict
from datetime import datetime



app = Flask(__name__)
app.secret_key = os.urandom(24)

RUTA_BASE = os.path.join('..', 'parte1', 'datos', 'json', 'revistas.json')
RUTA_INFO = os.path.join('..', 'parte2', 'datos_scrap', 'revistas_info.json')


# Cargar datos de revistas
with open(RUTA_BASE, 'r', encoding='latin-1') as f:
    revistas = json.load(f)

with open(RUTA_INFO, 'r', encoding='latin-1') as f:
    revistas_data = json.load(f)

AREAS = set()
CATALOGOS = set()

for revista_data in revistas.values():
    for area in revista_data.get('areas', []):
        AREAS.add(area)
    for catalogo in revista_data.get('catalogos', []):
        CATALOGOS.add(catalogo)

AREAS = sorted(list(AREAS))
CATALOGOS = sorted(list(CATALOGOS))

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
        catalogos_raw = revistas.get(titulo, {}).get('catalogos', [])
        if isinstance(catalogos_raw, str):
            catalogos_reales = [c.strip() for c in catalogos_raw.split(',')]
        else:
            catalogos_reales = catalogos_raw

        # Procesar letras iniciales
        if titulo:  # Asegurarse que el título no esté vacío
            letra_inicial = titulo[0].upper()
            if letra_inicial in abecedario:  # Solo si es una letra A-Z
                letras[letra_inicial].append({
                    'titulo': titulo,
                    'h_index': h_index,
                    'areas': subject_areas,
                    'catalogos': [catalogos_reales]
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
    return render_template('areas.html', areas=AREAS)

@app.route('/area/<area_name>')
def area_detail(area_name):
    revistas_area = []

    for titulo, datos in revistas.items():
        if area_name in datos.get('areas', []) and titulo in revistas_data:
            info = revistas_data[titulo]
            h_index = info.get('h_index', 'N/A')
            revistas_area.append({
                'titulo': titulo,
                'h_index': h_index
            })

    revistas_area.sort(key=lambda x: x['titulo'])

    return render_template('area_detail.html', area=area_name, revistas=revistas_area, now=datetime.now())

@app.route('/catalogos')
def catalogos():
    return render_template('catalogos.html', catalogos=CATALOGOS)

@app.route('/catalogo/<catalogo>')
def catalogo_detail(catalogo):
    revistas_catalogo = []

    for titulo, datos in revistas.items():
        if catalogo in datos.get('catalogos', []) and titulo in revistas_data:
            info = revistas_data[titulo]
            h_index = info.get('h_index', 'N/A')
            revistas_catalogo.append({
                'titulo': titulo,
                'h_index': h_index
            })

    revistas_catalogo.sort(key=lambda x: x['titulo'])

    return render_template('catalogo_detail.html', catalogo=catalogo, revistas=revistas_catalogo)

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

#Funcionabilidad extra inicio de sesion y guardado de favoritos
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Autenticación simple (en producción usar base de datos)
        if username and password:
            session['usuario'] = username
            flash(f'Bienvenido, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)