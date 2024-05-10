def export_to_tikz(graph):
    tikz_output = "\\begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=2.8cm,\n"
    tikz_output += "                    semithick]\n"

    node_labels = {}
    if isinstance(graph, list) and all(isinstance(x, list) for x in graph):  # Matrix
        num_nodes = len(graph)
        node_labels = {i: f"node{i+1}" for i in range(num_nodes)}
        for i in range(num_nodes):
            tikz_output += f"    \\node[state] ({node_labels[i]}) {{{i+1}}};\n"
        for i in range(num_nodes):
            for j in range(num_nodes):
                if graph[i][j] > 0:
                    tikz_output += f"    \\path ({node_labels[i]}) edge node {{}} ({node_labels[j]});\n"
    elif isinstance(graph, dict):  # List
        num_nodes = len(graph)
        node_labels = {node: f"node{node}" for node in graph}
        for node in graph:
            tikz_output += f"    \\node[state] ({node_labels[node]}) {{{node}}};\n"
        for node, edges in graph.items():
            for edge in edges:
                tikz_output += f"    \\path ({node_labels[node]}) edge node {{}} ({node_labels[edge]});\n"
    elif isinstance(graph, list) and all(isinstance(x, tuple) for x in graph):  # Table
        nodes = set(x for e in graph for x in e)
        node_labels = {node: f"node{node}" for node in nodes}
        for node in nodes:
            tikz_output += f"    \\node[state] ({node_labels[node]}) {{{node}}};\n"
        for src, dst in graph:
            tikz_output += f"    \\path ({node_labels[src]}) edge node {{}} ({node_labels[dst]});\n"

    tikz_output += "\\end{tikzpicture}"
    file_name = input("Enter filename for TikZ output (without extension): ")
    with open(f"{file_name}.tex", "w") as file:
        file.write(tikz_output)
    print(f"Graph exported to {file_name}.tex")

