from flask import Flask, render_template, request, jsonify
from logic import PeruGraph
from auxiliar.cargar_json import cargar_datos_desde_json
app = Flask(__name__)


#  datos JSON proporcionados
nodos_json, aristas_json = cargar_datos_desde_json('departamentos.json', 'carreteras.json')

peru_map = PeruGraph(nodos_json, aristas_json )

@app.route('/')
def index():
    nombres_deps = sorted([d['departamento'] for d in nodos_json])

    #Pasamos 'nodos_json' para que JS pueda dibujar los puntos al iniciar
    return render_template(
        'index.html', 
        deps=nombres_deps, #pasamos esto para la lista 
        departamentos_full=nodos_json #y esto para el dibujo o remarque de puntos
    )

@app.route('/api/ruta', methods=['POST'])
def obtener_ruta():
    data = request.json
    # Verificamos que los datos existan antes de procesar
    if not data or 'origen' not in data or 'destino' not in data:
        return jsonify({"error": "Faltan datos de origen o destino"}), 400
        
    resultado = peru_map.dijkstra(data['origen'], data['destino'])
    
    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({"error": "No se encontró una ruta entre estos puntos"}), 404

if __name__ == '__main__':
    app.run(debug=True)