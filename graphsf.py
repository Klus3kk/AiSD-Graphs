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
        print("--+" + "--" * len(graph))
        for i, row in enumerate(graph):
            print(f"{i + 1} | " + " ".join(str(val) for val in row))
    elif isinstance(graph, dict):  # List type
        for node, edges in graph.items():
            print(f"{node + 1}: {' '.join(str(edge + 1) for edge in edges)}")
    elif isinstance(graph, list) and all(isinstance(x, tuple) for x in graph):  # Table type
        print("Edges:")
        for src, dst in graph:
            print(f"{src + 1} -> {dst + 1}")


def find_edge(graph, from_node, to_node):
    try:
        if isinstance(graph, list):  # Matrix type
            exists = graph[from_node-1][to_node-1] > 0
        else:  # List or table type
            exists = to_node in graph[from_node]
        print(f"{'True' if exists else 'False'}: edge ({from_node}, {to_node}) {'exists' if exists else 'does not exist'} in the Graph!")
    except IndexError:
        print("Error: Node number out of valid range.")


def bfs(graph, start_node):
    from collections import deque
    visited = set()
    queue = deque([start_node - 1])  # Adjust to 0-based for internal processing
    bfs_order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            bfs_order.append(node + 1)  # Adjust back to 1-based for output
            if isinstance(graph, list):  # Matrix handling
                queue.extend(i for i, val in enumerate(graph[node]) if val > 0 and i not in visited)
            elif isinstance(graph, dict):  # List handling
                queue.extend(n - 1 for n in graph[node] if n - 1 not in visited)
            elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table handling
                neighbors = [e[1] - 1 for e in graph if e[0] - 1 == node]
                queue.extend(n for n in neighbors if n not in visited)

    return " ".join(map(str, bfs_order))

def dfs(graph, start_node, visited=None):
    if visited is None:
        visited = set()
    node = start_node - 1  # Adjust to 0-based for internal processing
    if node not in visited:
        print(start_node, end=' ')
        visited.add(node)
        if isinstance(graph, list):  # Matrix handling
            neighbors = [i for i, val in enumerate(graph[node]) if val > 0]
        elif isinstance(graph, dict):  # List handling
            neighbors = graph[node]
        elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table handling
            neighbors = [e[1] - 1 for e in graph if e[0] - 1 == node]

        for neighbor in neighbors:
            if neighbor not in visited:
                dfs(graph, neighbor + 1, visited)




def kahn_topological_sort(graph):
    from collections import deque
    in_degree = {}
    if isinstance(graph, list):  # Matrix representation
        in_degree = {i: 0 for i in range(len(graph))}
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] > 0:
                    in_degree[j] += 1
    elif isinstance(graph, dict):  # List representation
        in_degree = {i: 0 for i in range(len(graph))}
        for i in graph:
            for j in graph[i]:
                in_degree[j] += 1
    elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table representation
        nodes = set(x for e in graph for x in e)
        in_degree = {node: 0 for node in nodes}
        for (i, j) in graph:
            in_degree[j] += 1

    queue = deque([node for node in in_degree if in_degree[node] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node + 1)
        if isinstance(graph, list):  # Matrix
            for neighbor in range(len(graph[node])):
                if graph[node][neighbor] > 0:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
        elif isinstance(graph, dict):  # List
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        elif isinstance(graph, list) and all(isinstance(e, tuple) for e in graph):  # Table
            for (_, neighbor) in filter(lambda e: e[0] == node, graph):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    if len(sorted_order) != len(in_degree):
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


