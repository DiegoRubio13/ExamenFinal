import numpy as np
import heapq
import matplotlib.pyplot as plt

class Node:
    def __init__(self, position, g_cost, h_cost, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def get_neighbors(current, grid):
    neighbors = []
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:  
        new_pos = (current[0] + dx, current[1] + dy)
        if (0 <= new_pos[0] < grid.shape[0] and 
            0 <= new_pos[1] < grid.shape[1] and 
            grid[new_pos] > -1):  
            neighbors.append(new_pos)
    return neighbors

def get_path_cost(pos, grid):
    value = grid[pos]
    if value == 1: 
        return 1
    elif value == 2:  
        return 2
    elif value == 4:  
        return 4
    elif value == 5:  
        return 5
    return float('inf')  

def find_path(grid, start, goal):
    if grid[goal] < 0:
        print(f"Error: El punto final {goal} está en un obstáculo (valor: {grid[goal]})")
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_goal = (goal[0] + dx, goal[1] + dy)
                if (0 <= new_goal[0] < grid.shape[0] and 
                    0 <= new_goal[1] < grid.shape[1] and 
                    grid[new_goal] > 0):
                    print(f"Usando punto alternativo cercano como objetivo: {new_goal}")
                    goal = new_goal
                    break
            if grid[goal] > 0:
                break
        if grid[goal] < 0:
            print("No se encontró un punto válido cercano al objetivo")
            return None

    open_set = []
    closed_set = set()

    start_node = Node(start, 0, manhattan_distance(start, goal))
    heapq.heappush(open_set, start_node)

    nodes_explored = 0
    max_nodes = 10000

    while open_set and nodes_explored < max_nodes:
        current = heapq.heappop(open_set)
        nodes_explored += 1

        if nodes_explored % 100 == 0:
            print(f"Explorando... Nodos visitados: {nodes_explored}")

        if current.position == goal:
            print(f"¡Camino encontrado después de explorar {nodes_explored} nodos!")
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        closed_set.add(current.position)

        for neighbor_pos in get_neighbors(current.position, grid):
            if neighbor_pos in closed_set:
                continue

            g_cost = current.g_cost + get_path_cost(neighbor_pos, grid)
            h_cost = manhattan_distance(neighbor_pos, goal)

            neighbor = Node(neighbor_pos, g_cost, h_cost, current)

            if g_cost != float('inf'):
                heapq.heappush(open_set, neighbor)

    print(f"No se encontró camino después de explorar {nodes_explored} nodos")
    return None

def visualize_path(grid, path, start, goal):
    plt.figure(figsize=(12, 12))
    plt.imshow(grid, cmap='viridis')

    if path:
        path = np.array(path)
        plt.plot(path[:, 1], path[:, 0], 'r-', linewidth=2, label='Path')

    plt.plot(start[1], start[0], 'go', label='Start', markersize=15)
    plt.plot(goal[1], goal[0], 'ro', label='Goal', markersize=15)

    plt.colorbar(label='Street Condition')
    plt.legend()
    plt.grid(True)
    plt.title('Optimal Route from Home to Work')
    plt.show()

def main():
    try:
        grid = np.load('streets.npy')
        print("Grid cargado exitosamente")
        print("Forma del grid:", grid.shape)
        print("Valores únicos en el grid:", np.unique(grid))

        start = (5, 3)
        goal = (16, 26)
        print(f"\nValor en punto inicial {start}: {grid[start]}")
        print(f"Valor en punto final {goal}: {grid[goal]}")

        print("\nÁrea alrededor del inicio:")
        print(grid[max(0, start[0]-1):min(grid.shape[0], start[0]+2), 
              max(0, start[1]-1):min(grid.shape[1], start[1]+2)])
        print("\nÁrea alrededor del final:")
        print(grid[max(0, goal[0]-1):min(grid.shape[0], goal[0]+2), 
              max(0, goal[1]-1):min(grid.shape[1], goal[1]+2)])

        print("\nBuscando camino...")
        path = find_path(grid, start, goal)

        if path:
            print("\nCamino encontrado!")
            total_cost = sum(get_path_cost(pos, grid) for pos in path)
            print(f"Costo total: {total_cost}")
            print("Pasos del camino:")
            for i, pos in enumerate(path):
                print(f"Paso {i+1}: {pos} (costo: {get_path_cost(pos, grid)})")

            visualize_path(grid, path, start, goal)
        else:
            print("\nNo se pudo encontrar un camino")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()