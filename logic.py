import math
import heapq

class PeruGraph:
    def __init__(self, departamentos_json, conexiones_json):
        self.nodos = {d['departamento']: {'lat': d['lat'], 'lng': d['lng']} for d in departamentos_json}
        self.grafo = {d['departamento']: [] for d in departamentos_json}
        self.generar_aristas(conexiones_json)

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # Radio de la Tierra en km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def generar_aristas(self, conexiones):
        for u, v in conexiones:
            if u in self.nodos and v in self.nodos:
                n1, n2 = self.nodos[u], self.nodos[v]
                # Solo se crea la arista si existe en tu lista de carreteras
                peso = self.haversine(n1['lat'], n1['lng'], n2['lat'], n2['lng'])
                self.grafo[u].append((v, peso))
                self.grafo[v].append((u, peso))

    def dijkstra(self, inicio, fin):
        queue = [(0, inicio, [])]
        visitados = set()
        min_dist = {inicio: 0}

        while queue:
            (costo, actual, camino) = heapq.heappop(queue)

            if actual in visitados: continue
            
            #guardamos el nodo y tambien el costo acumulado hasta ese punto, al final lo mostraremos
            camino = camino + [(actual, costo)]

            if actual == fin:
                ruta_detallada = []

                for nombre, costo_acum in camino:
                    coord = self.get_coord(nombre)
                    coord['acumulado'] = round(costo_acum, 2) # Añadimos el peso al dict
                    ruta_detallada.append(coord)

                return {"ruta": ruta_detallada, "distancia": round(costo, 2)}

            visitados.add(actual)

            for (vecino, peso) in self.grafo.get(actual, []):
                if vecino in visitados: continue
                
                nuevo_costo = costo + peso
                if nuevo_costo < min_dist.get(vecino, float('inf')):
                    min_dist[vecino] = nuevo_costo
                    heapq.heappush(queue, (nuevo_costo, vecino, camino))
        return None

    def get_coord(self, nombre):
        return {"nombre": nombre, "lat": self.nodos[nombre]['lat'], "lng": self.nodos[nombre]['lng']}