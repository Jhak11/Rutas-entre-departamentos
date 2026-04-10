import json

def cargar_datos_desde_json(ruta_nodos, ruta_aristas):
    try:
        with open(ruta_nodos, 'r', encoding='utf-8') as f:
            nodos = json.load(f)
            
        with open(ruta_aristas, 'r', encoding='utf-8') as f:
            aristas = json.load(f)
            
        return nodos, aristas
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename}")
        return [], []
    except json.JSONDecodeError:
        print("Error: El formato del JSON es incorrecto.")
        return [], []