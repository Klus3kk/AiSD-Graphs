def export_to_tikz(graph):
    """
    Generates a TikZ representation of the graph. Handles matrix, list, and table graph types.

    :param graph: The graph in one of the supported formats (matrix, list, table).
    :return: A string containing the TikZ code.
    """
    tikz_output = "\\begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=2.8cm,\n"
    tikz_output += "                    semithick]\n"

    # Initialize node labels
    node_labels = {}
    if isinstance(graph, list) and all(isinstance(x, list) for x in graph):  # Matrix
        num_nodes = len(graph)
        node_labels = {i: f"node{i+1}" for i in range(num_nodes)}
        # Create TikZ nodes
        for i in range(num_nodes):
            tikz_output += f"    \\node[state] ({node_labels[i]}) {{{i+1}}};\n"
        # Create TikZ edges
        for i in range(num_nodes):
            for j in range(num_nodes):
                if graph[i][j] > 0:
                    tikz_output += f"    \\path ({node_labels[i]}) edge node {{}} ({node_labels[j]});\n"
    elif isinstance(graph, dict):  # List
        num_nodes = len(graph)
        node_labels = {node: f"node{node}" for node in graph}
        # Create TikZ nodes
        for node in graph:
            tikz_output += f"    \\node[state] ({node_labels[node]}) {{{node}}};\n"
        # Create TikZ edges
        for node, edges in graph.items():
            for edge in edges:
                tikz_output += f"    \\path ({node_labels[node]}) edge node {{}} ({node_labels[edge]});\n"
    elif isinstance(graph, list) and all(isinstance(x, tuple) for x in graph):  # Table
        nodes = set(x for e in graph for x in e)
        node_labels = {node: f"node{node}" for node in nodes}
        # Create TikZ nodes
        for node in nodes:
            tikz_output += f"    \\node[state] ({node_labels[node]}) {{{node}}};\n"
        # Create TikZ edges
        for src, dst in graph:
            tikz_output += f"    \\path ({node_labels[src]}) edge node {{}} ({node_labels[dst]});\n"

    tikz_output += "\\end{tikzpicture}"
    file_name = input("Enter filename for TikZ output (without extension): ")
    with open(f"{file_name}.tex", "w") as file:
        file.write(tikz_output)
    print(f"Graph exported to {file_name}.tex")

