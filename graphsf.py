import random
from collections import deque
def initialize_graph(num_nodes, graph_type, saturation=0):  
    graph = None
    if graph_type == 'matrix':
        graph = [[random.random() < saturation / 100.0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    elif graph_type == 'list':
        graph = {i + 1: [j for j in range(1, num_nodes + 1) if i != j - 1 and random.random() < saturation / 100.0] for i in range(num_nodes)}
    elif graph_type == 'table':
        graph = [(i, j) for i in range(1, num_nodes + 1) for j in range(1, num_nodes + 1) if i != j and random.random() < saturation / 100.0]
    return graph


def print_graph(graph):
    if isinstance(graph, list) and all(isinstance(x, list) for x in graph):  # Matrix type
        num_rows = len(graph)
        max_index_digits = len(str(num_rows))

        header = ' ' * (max_index_digits + 2)  
        for i in range(1, num_rows + 1):
            header += f"{i:>{3}}"  

        print(header)

        print('-' * (max_index_digits + 1) + '+' + '-' * (len(header) - max_index_digits - 2))

        for i, row in enumerate(graph):
            row_str = f"{i+1:>{max_index_digits}} |"  
            for val in row:
                row_str += f"{val:>{3}}"  
            print(row_str)
            
    elif isinstance(graph, dict):  # List type
        max_node = max(graph.keys(), default=0)  
        for node in range(1, max_node + 1):
            edges = " ".join(str(edge) for edge in graph.get(node, []))
            print(f"{node}: {edges}")
    elif isinstance(graph, list) and all(isinstance(x, tuple) for x in graph):  
        print("Edges:")
        for src, dst in graph:
            print(f"{src} -> {dst}")

def find_path(graph, from_node, to_node):
    if isinstance(graph, list):
        if all(isinstance(row, list) for row in graph):
            return graph[from_node - 1][to_node - 1] > 0
        elif all(isinstance(edge, tuple) for edge in graph):
            return (from_node, to_node) in graph
    elif isinstance(graph, dict):
        return to_node in graph.get(from_node, [])

    return False


def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    bfs_order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            bfs_order.append(node)
            if isinstance(graph, list) and all(isinstance(row, list) for row in graph):  # Matrix
                neighbors = [i + 1 for i, val in enumerate(graph[node - 1]) if val > 0]
            elif isinstance(graph, dict):  # List
                neighbors = graph.get(node, [])
            elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table
                neighbors = [dst for src, dst in graph if src == node]

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)

    return " ".join(map(str, bfs_order))

def dfs(graph, start_node, visited=None):
    if visited is None:
        visited = set()

    stack = [start_node]

    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=' ')
            visited.add(node)

            if isinstance(graph, list) and all(isinstance(row, list) for row in graph):
                neighbors = [i + 1 for i, val in enumerate(graph[node - 1]) if val > 0]
            elif isinstance(graph, dict):
                neighbors = graph.get(node, [])
            elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):
                neighbors = [dst for src, dst in graph if src == node]

            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

def kahn_topological_sort(graph):
    in_degree = {}
    nodes = set()

    if isinstance(graph, list) and all(isinstance(x, list) for x in graph):  # Matrix
        nodes = set(range(1, len(graph)+1))
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                in_degree[j+1] = in_degree.get(j+1, 0) + (1 if graph[i][j] > 0 else 0)
    elif isinstance(graph, dict):  # List
        nodes = set(graph.keys())
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
    elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table
        nodes = set(x for e in graph for x in e)
        for src, dst in graph:
            in_degree[dst] = in_degree.get(dst, 0) + 1

    queue = deque([node for node in nodes if in_degree.get(node, 0) == 0])
    sorted_order = []
    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        if isinstance(graph, list) and all(isinstance(x, list) for x in graph):  # Matrix
            for neighbor in range(1, len(graph[node-1])+1):
                if graph[node-1][neighbor-1] > 0:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
        elif isinstance(graph, dict):  # List
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table
            for src, dst in filter(lambda e: e[0] == node, graph):
                in_degree[dst] -= 1
                if in_degree[dst] == 0:
                    queue.append(dst)

    if len(sorted_order) != len(nodes):
        raise Exception("Graph has at least one cycle")
    return sorted_order


def tarjan_scc(graph):
    current_index = 0
    recursion_stack = []
    node_indices = {}
    lowest_links = {}
    in_stack = {}
    components = []

    def explore_node(node):
        nonlocal current_index
        node_indices[node] = lowest_links[node] = current_index
        current_index += 1
        recursion_stack.append(node)
        in_stack[node] = True

        neighbors = []
        if isinstance(graph, list) and all(isinstance(row, list) for row in graph):  # Matrix
            neighbors = [j + 1 for j, val in enumerate(graph[node - 1]) if val > 0]
        elif isinstance(graph, dict):  # List
            neighbors = graph.get(node, [])
        elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table 
            neighbors = [destination for source, destination in graph if source == node]

        for neighbor in neighbors:
            if neighbor not in node_indices:
                explore_node(neighbor)
                lowest_links[node] = min(lowest_links[node], lowest_links[neighbor])
            elif in_stack[neighbor]:
                lowest_links[node] = min(lowest_links[node], node_indices[neighbor])

        if lowest_links[node] == node_indices[node]:
            component = []
            while True:
                w = recursion_stack.pop()
                in_stack[w] = False
                component.append(w)
                if w == node:
                    break
            components.append(component)

    if isinstance(graph, list) and all(isinstance(row, list) for row in graph):
        node_set = range(1, len(graph) + 1)
    elif isinstance(graph, dict):
        node_set = graph.keys()
    elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):
        node_set = set(src for src, _ in graph).union(dst for _, dst in graph)

    for node in node_set:
        if node not in node_indices:
            explore_node(node)

    return components

    