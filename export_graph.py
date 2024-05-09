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
    if isinstance(graph, list):  # Matrix
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
    else:  # List or Table
        node_labels = {node: f"node{node}" for node in graph}
        # Create TikZ nodes
        for node in graph:
            tikz_output += f"    \\node[state] ({node_labels[node]}) {{{node}}};\n"
        # Create TikZ edges
        for node, edges in graph.items():
            for edge in edges:
                tikz_output += f"    \\path ({node_labels[node]}) edge node {{}} ({node_labels[edge]});\n"

    tikz_output += "\\end{tikzpicture}"
    return tikz_output
