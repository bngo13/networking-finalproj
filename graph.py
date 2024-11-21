vertexMap = {}

def fileParser(fileName):
    f = open(fileName, "r")

    count = 0
    graphSize = (len(f.readlines()))
    userGraph = Graph(graphSize)
    f.seek(0)
    for line in f:
        nodeData = line.split(" ")
        vertexMap[nodeData[0]] = count
        userGraph.add_vertex_data(count, nodeData[0])
        count += 1
    f.seek(0)
    for line in f:
        nodeData = line.strip().split(" ")
        for edge in nodeData[1:]:
            edgeCost = edge.split("-")
            userGraph.add_edge(vertexMap[nodeData[0]], vertexMap[edgeCost[0]], int(edgeCost[1]))
    f.seek(0)
    print(vertexMap)
    return userGraph


class Edge:
    def __init__(self, weight):
        self.isUp = True
        self.weight = weight

    def getWeight(self):
        if not self.isUp:
            return float('inf')

        return self.weight
    
    def setDown(self):
        self.isUp = False
    
    def setUp(self):
        self.isUp = True

class Graph:
    # Inspired by https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php
    def __init__(self, size):
        self.adj_matrix = [[Edge(0)] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def down_node(self, node):
        for neighbors in self.adj_matrix[node]:
            neighbors.setDown()
    
    def restore_node(self, node):
        for neighbors in self.adj_matrix[node]:
            neighbors.setUp()

    def add_edge(self, currentNode, neighborNode, cost):
        if 0 <= currentNode < self.size and 0 <= neighborNode < self.size:
            edge = Edge(cost)
            self.adj_matrix[currentNode][neighborNode] = edge
            self.adj_matrix[neighborNode][currentNode] = edge

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, startNodeIndex):
        startNode = self.vertex_data.index(startNodeIndex)
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[startNode] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            min_distance = float('inf')
            currentNode = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    currentNode = i

            if currentNode is None:
                break

            visited[currentNode] = True

            for neighborNode in range(self.size):
                if self.adj_matrix[currentNode][neighborNode].getWeight() != 0 and not visited[neighborNode]:
                    alternativeDistance = distances[currentNode] + self.adj_matrix[currentNode][neighborNode].getWeight()
                    if alternativeDistance < distances[neighborNode]:
                        distances[neighborNode] = alternativeDistance
                        predecessors[neighborNode] = currentNode

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

def menu():
    choice = input("Do you want to setup your own graph or use the default one (setup or default)? ")
    if choice == "default":
        g = fileParser("default_input.txt")
    else:
        fileName = input("Enter file with the chosen graph: ")
        g = fileParser(fileName)
    
    sourceNode = input("What will be the source node? ")
    destinationNode = input("what will be the destination node? ")

    while True:
        print("Calculating paths...")
        # Dijkstra's algorithm from D to all vertices
        print("Dijkstra's Algorithm starting from vertex D:\n")
        distances, predecessors = g.dijkstra(sourceNode)
        print(distances)
        for i, d in enumerate(distances):
            print(f"Shortest distance from U to {g.vertex_data[i]}: {d}")
            path = g.get_path(predecessors, 'U', g.vertex_data[i])
            print(path)
        

   

