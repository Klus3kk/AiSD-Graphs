import sys
from graphsf import *
from export_graph import *

def display_help():
    print("\nAvailable commands:")
    print("Help       - Show this message")
    print("Find       - Print the edge of the graph from the selected node to the second selected node")
    print("Print      - Print the graph in selected representation")        
    print("BFS        - Executes Breadth-First Search")
    print("DFS        - Executes Depth-First Search")
    print("Kahn       - Executes Kahn's algorithm for topological sorting.")
    print("Tarjan     - Executes Tarjan's algorithm to find strongly connected components.")
    print("Export     - Export the graph to TikZ picture")
    print("Exit       - Exit the program (same as ctrl+C)")

def process_command(command, graph, graph_type):
    args = command.split()
    cmd = args[0].lower()

    if cmd == 'help':
        display_help()
        
    elif cmd == 'find':
        from_node, to_node = int(args[1]), int(args[2])
        exists = find_edge(graph, from_node, to_node)
        if exists:
            print(f"True: edge ({from_node},{to_node}) exists in the Graph!")
        else:
            print(f"False: edge ({from_node},{to_node}) does not exist in the Graph!")
            
    elif cmd == 'print':
        print_graph(graph)
        
    elif cmd == 'bfs':
        start_node = int(args[1]) if len(args) > 1 else 0
        result = bfs(graph, start_node)
        print("BFS order from node", start_node, ":", result)

    elif cmd == 'dfs':
        start_node = int(args[1]) if len(args) > 1 else 0
        print("DFS order from node", start_node, ": ", end='')
        dfs(graph, start_node)
        print()  # for newline

    elif cmd == 'kahn':
        try:
            print('Kahn Topological Sort:', kahn_topological_sort(graph))
        except Exception as e:
            print(f"Error: {e}")
            
    elif cmd == 'tarjan':
        print('Strongly Connected Components:', tarjan_scc(graph))
        
    elif cmd == 'export':
        print(export_to_tikz(graph))
        
    elif cmd == 'exit':
        print('Exiting...')
        sys.exit(0)
    else:
        print('Invalid command. Type "help" for a list of commands.')

def main():
    if len(sys.argv) != 2 or (sys.argv[1] not in ['--generate', '--user-provided']):
        print("Usage: python3 main.py --generate or python3 main.py --user-provided")
        sys.exit(1)

    print("Choose graph representation ('matrix', 'list', 'table'):")
    graph_type = input('type> ').lower()
    if graph_type not in ['matrix', 'list', 'table']:
        print("Invalid graph type specified.")
        sys.exit(1)

    num_nodes = int(input('nodes> '))
    
    # Ask for saturation only if --generate is used
    if sys.argv[1] == '--generate':
        saturation = float(input('saturation> '))
        graph = initialize_graph(num_nodes, graph_type, saturation)
    else:
        graph = initialize_graph(num_nodes, graph_type)

    if sys.argv[1] == '--user-provided':
        for i in range(num_nodes):
            valid_input = False
            while not valid_input:
                edges = input(f'{i + 1}> ')
                try:
                    input_nodes = list(map(int, edges.split()))
                    if any(node < 1 or node > num_nodes for node in input_nodes):
                        print("Error: Node numbers must be within the valid range. Please re-enter.")
                    elif len(input_nodes) != len(set(input_nodes)):
                        print("Error: Duplicate nodes detected. Please re-enter.")
                    else:
                        valid_input = True
                        if graph_type == 'matrix':
                            for j in input_nodes:
                                graph[i][j - 1] = 1
                        elif graph_type in ['list', 'table']:
                            graph[i] = input_nodes
                except ValueError:
                    print("Invalid input. Please enter integer values only.")

    
    # Now process commands
    while True:
        try:
            command = input('\naction> ')
            process_command(command, graph, graph_type)  
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
