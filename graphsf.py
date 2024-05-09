import random

def initialize_graph(num_nodes, graph_type, saturation=None):
    graph = None
    if graph_type == 'matrix':
        graph = [[0] * num_nodes for _ in range(num_nodes)]
        if saturation:
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if random.random() < saturation / 100.0:
                        graph[i][j] = 1
    elif graph_type == 'list':
        graph = {i: [] for i in range(num_nodes)}
        if saturation:
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if random.random() < saturation / 100.0:
                        graph[i].append(j)
    elif graph_type == 'table':
        graph = []
        if saturation:
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if random.random() < saturation / 100.0:
                        graph.append((i, j))
    return graph




def print_graph(graph):
    if isinstance(graph, list) and all(isinstance(x, list) for x in graph):  # Matrix type
        print("  | " + " ".join(str(i + 1) for i in range(len(graph))))
        print("--+" + "-" * 3 * len(graph))
        for i, row in enumerate(graph):
            print(f"{i + 1} | " + " ".join(str(val) for val in row))
    elif isinstance(graph, dict):  # List type
        # Ensure printing starts from node 1 and includes all nodes, even if they have no edges
        max_node = max(graph.keys(), default=0)  # In case the dictionary is empty
        for node in range(1, max_node + 1):
            edges = " ".join(str(edge) for edge in graph.get(node, []))
            print(f"{node}: {edges}")
    elif isinstance(graph, list) and all(isinstance(x, tuple) for x in graph):  # Table type
        print("Edges:")
        for src, dst in graph:
            print(f"{src} -> {dst}")




def find_path(graph, from_node, to_node):
    if isinstance(graph, list):
        # Check if it's a matrix (2D list)
        if all(isinstance(row, list) for row in graph):
            # Matrix - assuming 0-indexed, adjust if 1-indexed
            return graph[from_node - 1][to_node - 1] > 0
        # Check if it's a table (list of tuples)
        elif all(isinstance(edge, tuple) for edge in graph):
            # Table - list of tuples (from, to)
            return (from_node, to_node) in graph
    elif isinstance(graph, dict):
        # List - adjacency list
        return to_node in graph.get(from_node, [])

    return False




def bfs(graph, start_node):
    from collections import deque
    visited = set()
    queue = deque([start_node])
    bfs_order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            bfs_order.append(node)
            # Handle graph types accordingly
            if isinstance(graph, list):  # Matrix handling
                queue.extend(i + 1 for i, val in enumerate(graph[node - 1]) if val > 0 and (i + 1) not in visited)
            elif isinstance(graph, dict):  # List handling
                queue.extend(n for n in graph.get(node, []) if n not in visited)
            elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table handling
                neighbors = [dst for src, dst in graph if src == node and dst not in visited]
                queue.extend(neighbors)

    return " ".join(map(str, bfs_order))



def dfs(graph, start_node, visited=None):
    if visited is None:
        visited = set()
    if start_node not in visited:
        print(start_node, end=' ')
        visited.add(start_node)
        neighbors = []
        if isinstance(graph, list):  # Matrix handling
            neighbors = [i + 1 for i, val in enumerate(graph[start_node - 1]) if val > 0]
        elif isinstance(graph, dict):  # List handling
            neighbors = graph.get(start_node, [])
        elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table handling
            neighbors = [dst for src, dst in graph if src == start_node]
        for neighbor in neighbors:
            if neighbor not in visited:
                dfs(graph, neighbor, visited)






def kahn_topological_sort(graph):
    from collections import deque
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
        raise Exception("Graph has at least one cycle, which prevents topological sorting.")
    return sorted_order



def tarjan_scc(graph):
    index = 0
    stack = []
    indices = {}
    low_links = {}
    on_stack = {}
    scc = []

    def strongconnect(node):
        nonlocal index
        indices[node] = index
        low_links[node] = index
        index += 1
        stack.append(node)
        on_stack[node] = True

        # Determine neighbors based on graph type
        if isinstance(graph, list):  # Matrix handling
            neighbors = [i for i, val in enumerate(graph[node]) if val > 0]
        elif isinstance(graph, dict):  # List handling
            neighbors = graph[node]
        elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table handling
            neighbors = [e[1] for e in graph if e[0] == node]

        for neighbor in neighbors:
            if neighbor not in indices:
                strongconnect(neighbor)
                low_links[node] = min(low_links[node], low_links[neighbor])
            elif on_stack[neighbor]:
                low_links[node] = min(low_links[node], indices[neighbor])

        if low_links[node] == indices[node]:
            connected_component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                connected_component.append(w + 1)  # Adjust back to 1-based for output
                if w == node:
                    break
            scc.append(connected_component)

    for node in range(len(graph)):  # Assumption: nodes are 0-indexed
        if node not in indices:
            strongconnect(node)

    return scc


