import numpy as np
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from paste import Node, find_path, get_path_cost

class PathfindingAgent:
    def __init__(self, start_pos, goal_pos, grid):
        self.position = start_pos
        self.initial_start = start_pos
        self.goal = goal_pos
        self.grid = grid
        self.path = None
        self.current_step = 0
        self.has_started = False
        print(f"Iniciando agente en {start_pos} hacia {goal_pos}")
        self.calculate_path()
    
    def calculate_path(self):
        if not self.has_started:
            print("Calculando path inicial...")
            self.path = find_path(self.grid, self.initial_start, self.goal)
            if self.path:
                print(f"Path encontrado con {len(self.path)} pasos")
            self.has_started = True
        
    def update(self):
        if self.path and self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.position = self.path[self.current_step]
            return True
        else:
          
            self.current_step = 0
            self.position = self.initial_start
        return False
    
    def get_state(self):
        current_pos = self.path[self.current_step] if self.path else self.position
        return {
            "position": {
                "x": float(current_pos[1]),
                "y": 0.5,
                "z": float(current_pos[0])
            },
            "grid": self.grid.tolist(),  
            "path": [{"x": float(p[1]), "y": 0.5, "z": float(p[0])} for p in self.path] if self.path else []
        }

class MultiAgentSystem:
    def __init__(self):
        print("Cargando grid...")
        self.grid = np.load('streets.npy')
        print(f"Grid cargado. Forma: {self.grid.shape}")
        print(f"Valores únicos en el grid: {np.unique(self.grid)}")
        self.agents = []
        self.setup_agents()
    
    def setup_agents(self):
        start = (5, 3)
        goal = (15, 25)  
        print(f"Creando agente: inicio={start}, meta={goal}")
        agent = PathfindingAgent(start, goal, self.grid)
        self.agents.append(agent)
    
    def update(self):
        states = []
        for agent in self.agents:
            agent.update()
            states.append(agent.get_state())
        return states

class Server(BaseHTTPRequestHandler):
    mas = MultiAgentSystem()
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def do_GET(self):
        try:
            self._set_response()
            states = self.mas.update()
            response = {"agents": states}
            response_json = json.dumps(response)
            print("Enviando respuesta al cliente...")
            self.wfile.write(response_json.encode('utf-8'))
        except Exception as e:
            print(f"Error en do_GET: {e}")
            raise

def run_server(server_class=HTTPServer, handler_class=Server, port=8585):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor en puerto {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Servidor detenido")

if __name__ == '__main__':
    run_server()