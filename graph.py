class Edge:
    def __init__(self, weight):
        self.isUp = True
        self.weight = weight

    def getWeight(self):
        if not self.isUp:
            return float('inf')

        return self.weight

class Graph:
    # Inspired by https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php
    def __init__(self, size):
        self.adj_matrix = [[Edge(0)] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = Edge(weight)
            self.adj_matrix[v][u] = Edge(weight)

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data):
        start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i

            if u is None:
                break

            visited[u] = True

            for v in range(self.size):
                if self.adj_matrix[u][v].getWeight() != 0 and not visited[v]:
                    alt = distances[u] + self.adj_matrix[u][v].getWeight()
                    if alt < distances[v]:
                        distances[v] = alt
                        predecessors[v] = u
        
        return distances, predecessors
    def get_path(self, predecessors, start_vertex, end_vertex):
        path = []
        current = self.vertex_data.index(end_vertex)
        while current is not None:
            path.insert(0, self.vertex_data[current])
            current = predecessors[current]
            if current == self.vertex_data.index(start_vertex):
                path.insert(0, start_vertex)
                break
        return '->'.join(path)  # Join the vertices with '->'

g = Graph(6)

g.add_vertex_data(0, 'U')
g.add_vertex_data(1, 'V')
g.add_vertex_data(2, 'X')
g.add_vertex_data(3, 'W')
g.add_vertex_data(4, 'Y')
g.add_vertex_data(5, 'Z')

g.add_edge(0, 1, 2)  # U -> V 2
g.add_edge(0, 2, 1)  # U -> X 1
g.add_edge(0, 3, 5)  # U -> W 5
g.add_edge(1, 2, 2)  # V -> X 2
g.add_edge(1, 3, 3)  # V -> W 3
g.add_edge(2, 3, 3)  # X -> W 3
g.add_edge(2, 4, 1)  # X -> Y 1
g.add_edge(3, 4, 1)  # W -> Y 1
g.add_edge(3, 5, 5)  # W -> Z 5
g.add_edge(4, 5, 2)  # Y -> Z 2

# Dijkstra's algorithm from D to all vertices
print("Dijkstra's Algorithm starting from vertex D:\n")
distances, predecessors = g.dijkstra('U')
for i, d in enumerate(distances):
    print(f"Shortest distance from U to {g.vertex_data[i]}: {d}")
    path = g.get_path(predecessors, 'U', g.vertex_data[i])
    print(path)