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
    print("Exit       - Exit the program (same as Ctrl+C)")

def process_command(command, graph, graph_type):
    args = command.split()
    cmd = args[0].lower()

    if cmd == 'help':
        display_help()
    elif cmd == 'find':
        try:
            from_node = int(input("from> "))
            to_node = int(input("to> "))
            exists = find_path(graph, from_node, to_node)
            print(f"True: edge ({from_node}, {to_node}) exists in the Graph!" if exists else f"False: edge ({from_node}, {to_node}) does not exist in the Graph!")
        except ValueError:
            print("Error: Both 'from' and 'to' nodes must be integers.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    elif cmd == 'print':
        print_graph(graph)
    elif cmd == 'bfs':
        try:
            start_node = int(input("Start node for BFS: "))
            print(f"BFS order from node {start_node}: ", bfs(graph, start_node))
        except ValueError:
            print("Invalid input for the start node.")
        except KeyError:
            print(f"Node {start_node} does not exist in the graph.")
    elif cmd == 'dfs':
        try:
            start_node = int(input("Start node for DFS: "))
            print("DFS order from node {}: ".format(start_node), end='')
            dfs(graph, start_node)
            print()
        except ValueError:
            print("Invalid input for the start node.")
        except KeyError:
            print(f"Node {start_node} does not exist in the graph.")
    elif cmd == 'kahn':
        try:
            print('Kahn:', kahn_topological_sort(graph))
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == 'tarjan':
        try:
            print('Tarjan:', tarjan_scc(graph))
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == 'export':
        export_to_tikz(graph)
    elif cmd == 'exit':
        print('Exiting...')
        sys.exit(0)
    else:
        print('Invalid command. Type "help" for a list of commands.')

def main():
    if len(sys.argv) != 2 or (sys.argv[1] not in ['--generate', '--user-provided']):
        print("Usage: python3 main.py --generate or python3 main.py --user-provided")
        sys.exit(1)

    graph_type = input("Choose graph representation ('matrix', 'list', 'table'): \ntype> ").lower()
    if graph_type not in ['matrix', 'list', 'table']:
        print("Invalid graph type specified.")
        sys.exit(1)

    while True:
        try:
            num_nodes = int(input('nodes> '))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for number of nodes.")

    if sys.argv[1] == '--generate':
        while True:
            try:
                saturation = float(input('saturation> '))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for saturation.")

        graph = initialize_graph(num_nodes, graph_type, saturation)
    else:
        graph = initialize_graph(num_nodes, graph_type)

    if sys.argv[1] == '--user-provided':
        if graph_type == 'table':
            graph = []
        else:
            graph = initialize_graph(num_nodes, graph_type)

        for i in range(1, num_nodes + 1):
            valid_input = False
            while not valid_input:
                edges = input(f'{i}> ')
                try:
                    input_nodes = list(map(int, edges.split()))
                    if any(node < 1 or node > num_nodes for node in input_nodes):
                        print("Error: Node numbers must be within the valid range. Please re-enter.")
                    elif len(set(input_nodes)) != len(input_nodes):
                        print("Error: Duplicate nodes detected. Please re-enter.")
                    else:
                        valid_input = True
                        if graph_type == 'matrix':
                            graph[i-1] = [0] * num_nodes
                            for j in input_nodes:
                                graph[i-1][j-1] = 1
                        elif graph_type == 'list':
                            graph[i] = input_nodes
                        elif graph_type == 'table':
                            for j in input_nodes:
                                graph.append((i, j))  
                except ValueError:
                    print("Invalid input. Please enter integer values only.")

    while True:
        try:
            command = input('\naction> ')
            process_command(command, graph, graph_type)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
