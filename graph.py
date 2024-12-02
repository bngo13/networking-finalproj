# dependencies
import networkx as nx
import matplotlib.pyplot as plt

vertexMap = {} # map that keeps all vertices and enumerate them

def fileParser(fileName):
    """
    Parses a file to construct a graph and a mapping of vertex names to indices.

    Args:
        fileName (str): Name of the file containing graph data.

    Returns:
        Graph: A Graph object populated with vertex and edge data from the file.
    """
    f = open(fileName, "r")
    count = 0
    graphSize = len(f.readlines())  # Determine the number of vertices
    userGraph = Graph(graphSize)
    f.seek(0)  # Reset file pointer to beginning

    # Map vertex names to indices and populate graph vertex data
    for line in f:
        nodeData = line.split(" ")
        vertexMap[nodeData[0]] = count
        userGraph.add_vertex_data(count, nodeData[0])
        count += 1

    f.seek(0)  # Reset file pointer again to read edges
    for line in f:
        nodeData = line.strip().split(" ")
        for edge in nodeData[1:]:
            edgeCost = edge.split("-")
            userGraph.add_edge(vertexMap[nodeData[0]], vertexMap[edgeCost[0]], int(edgeCost[1]))

    return userGraph

class Edge:
    """
    Represents an edge in a graph with a weight and status (up or down).
    """
    def __init__(self, weight):
        """
        Initialize an edge with a weight and default status as 'up'.

        Args:
            weight (int): The weight of the edge.
        """
        self.isUp = True
        self.weight = weight

    def getWeight(self):
        """
        Get the effective weight of the edge. If the edge is down, returns infinity.

        Returns:
            int: The weight of the edge or infinity if down.
        """
        if not self.isUp:
            return float('inf')
        return self.weight
    
    def setDown(self):
        """Set the edge status to down (disabled)."""
        self.isUp = False
    
    def setUp(self):
        """Set the edge status to up (enabled)."""
        self.isUp = True

class Graph:
    """
    Represents a graph using an adjacency matrix for edges and a list for vertex data.
    """
    def __init__(self, size):
        """
        Initialize a graph with a given number of vertices.

        Args:
            size (int): Number of vertices in the graph.
        """
        self.adj_matrix = [[Edge(0)] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def down_node(self, node):
        """
        Disable all edges for a given node.

        Args:
            node (int): The index of the node to disable.
        """
        for neighbors in self.adj_matrix[node]:
            neighbors.setDown()
    
    def restore_node(self, node):
        """
        Enable all edges for a given node.

        Args:
            node (int): The index of the node to enable.
        """
        for neighbors in self.adj_matrix[node]:
            neighbors.setUp()

    def add_edge(self, currentNode, neighborNode, cost):
        """
        Add an edge between two nodes with a specified weight.

        Args:
            currentNode (int): The index of the current node.
            neighborNode (int): The index of the neighbor node.
            cost (int): The weight of the edge.
        """
        if 0 <= currentNode < self.size and 0 <= neighborNode < self.size:
            edge = Edge(cost)
            self.adj_matrix[currentNode][neighborNode] = edge
            self.adj_matrix[neighborNode][currentNode] = edge

    def add_vertex_data(self, vertex, data):
        """
        Add data to a vertex.

        Args:
            vertex (int): The index of the vertex.
            data (str): The data to associate with the vertex.
        """
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, startNodeIndex):
        """
        Perform Dijkstra's algorithm to find the shortest paths from a starting node.

        Args:
            startNodeIndex (int): The index of the starting node.

        Returns:
            tuple: A tuple containing distances and predecessors for all nodes.
        """
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[startNodeIndex] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            # Find the unvisited node with the smallest distance
            min_distance = float('inf')
            currentNode = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    currentNode = i

            if currentNode is None:
                break

            visited[currentNode] = True

            # Update distances to neighbors
            for neighborNode in range(self.size):
                edge_weight = self.adj_matrix[currentNode][neighborNode].getWeight()
                if edge_weight != 0 and not visited[neighborNode]:
                    alternativeDistance = distances[currentNode] + edge_weight
                    if alternativeDistance < distances[neighborNode]:
                        distances[neighborNode] = alternativeDistance
                        predecessors[neighborNode] = currentNode

        return distances, predecessors

    def get_path(self, predecessors, start_vertex, end_vertex):
        """
        Reconstruct the shortest path from the predecessors list.

        Args:
            predecessors (list): List of predecessor nodes for each node.
            start_vertex (str): The starting vertex name.
            end_vertex (str): The destination vertex name.

        Returns:
            str: The shortest path as a string of vertex names.
            list: A list of edges in the shortest path.
        """
        path = []
        path_edges = []
        current = vertexMap[end_vertex]
        # Go backwards from destination node to start node to construct the path
        while current is not None:
            path.insert(0, self.vertex_data[current])
            if current != vertexMap[end_vertex]:
                path_edges.insert(0, (self.vertex_data[predecessors[current]], self.vertex_data[current]))  # Add edge to path_edges
            current = predecessors[current]
            if current == vertexMap[start_vertex]:
                path.insert(0, start_vertex)
                break
            
        if path:
            path_edges.insert(0, (path[-2], path[-1]))  # Add the final edge from the last node to destination
        
        return '->'.join(path), path_edges
    
    def drawGraph(self, pathEdges=None):
        """
        Draw the graph using the networkx library, with optional highlighting for edges.

        Args:
            pathEdges (list): A list of edges (tuples) to highlight.
        """
        G = nx.Graph()
        options = {
            "font_size": 36,
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 5,
            "width": 5,
        }

        for i in range(self.size):
            G.add_node(self.vertex_data[i])
            for j in range(self.size):
                if self.adj_matrix[i][j].weight != 0:
                    G.add_edge(self.vertex_data[i], self.vertex_data[j], weight=self.adj_matrix[i][j].weight)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')

        # Draw the highlighted edges of the best path
        if pathEdges:
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=pathEdges,
                edge_color='red',
                width=10,
            )

        nx.draw(G, pos, with_labels=True, **options)
        
        label_pos = {}
        for key, value in pos.items():
            # Shifts the position of the labels
            label_pos[key] = (value[0], value[1] + 0.05)

        nx.draw_networkx_edge_labels(G, label_pos, edge_labels=labels, font_size=12, font_color="black")
        
        plt.show()

def menu():
    """
    Display a menu for the user to interact with the graph and perform operations.
    """
    choice = input("Do you want to use your own graph or use the default one (own or default)? ")
    if choice == "default":
        g = fileParser("default_input.txt")
    elif choice == "own":
        fileName = input("Enter file with the chosen graph: ")
        g = fileParser(fileName)
    else:
        print("Invalid Input! Using the default graph for now")
        g = fileParser("default_input.txt")
    
    sourceNode = input("Choose a source node? ")
    while sourceNode not in vertexMap:
        sourceNode = input("Invalid Node!\nChoose a source node? ")

    destinationNode = input("Choose a destination node? ")
    while destinationNode not in vertexMap:
        destinationNode = input("Invalid Node!\nChoose a destination node? ")

    while True:
        actionChoice = input("(a) Find shortest path\n(b) Down a node\n(c) Restore a node\n(q) Exit\nChoice: ")
        print()
        match actionChoice:
            case "a":
                distances, predecessors = g.dijkstra(vertexMap[sourceNode])
                pathCost = distances[vertexMap[destinationNode]]

                # Only show the path if it is reachable
                if pathCost == float('inf'):
                    print(f"{sourceNode} to {destinationNode} is unreachable. Cost is: {pathCost}\n")
                    continue

                print(f"Shortest distance from {sourceNode} to {destinationNode} is: {pathCost}")
                pathString, pathEdges = g.get_path(predecessors, sourceNode, destinationNode)
                print(f"Path from {sourceNode} to {destinationNode}: {pathString}\n")
                g.drawGraph(pathEdges)

            case "b":
                downNodeChoice = input("Which node do you want to down? ")
                while downNodeChoice not in vertexMap:
                    downNodeChoice = input("Invalid node! Please enter existing node\nWhich node do you want to down? ")
                g.down_node(vertexMap[downNodeChoice])
            case "c":
                restoreNodeChoice = input("Which node do you want to restore? ")
                while restoreNodeChoice not in vertexMap:
                    restoreNodeChoice = input("Invalid node! Please enter existing node\nWhich node do you want to restore? ")
                g.restore_node(vertexMap[restoreNodeChoice])
            case "q":
                print("Exiting the program...")
                break
            case _:
                print("Invalid Input! Please try again.")
        
menu()
