# networkX_draw.py
import networkx as nx
import matplotlib.pyplot as plt

def draw_linear(num_vms):
    G = nx.Graph()
    for i in range(num_vms - 1):
        G.add_edge(f'VM{i}', f'VM{i+1}')
    nx.draw(G, with_labels=True)
    plt.show()

def draw_mesh(num_vms):
    G = nx.grid_2d_graph(int(num_vms**0.5), int(num_vms**0.5))
    nx.draw(G, with_labels=True)
    plt.show()

def draw_custom_tree(num_vms):
    G = nx.Graph()
    nodes_to_add = [(0, i + 1) for i in range(2)]
    node_counter = 3  # Comienza en 3 porque ya tenemos 3 nodos en 'nodes_to_add'

    G.add_edges_from(nodes_to_add)  # Agrega los primeros nodos y aristas

    while node_counter < num_vms:
        new_nodes_to_add = []
        for parent, _ in nodes_to_add:
            for i in range(2):  # Cada nodo padre tiene dos hijos
                if node_counter >= num_vms:
                    break  # Salimos del bucle si alcanzamos el número de nodos deseado
                new_nodes_to_add.append((parent, node_counter))
                node_counter += 1
        G.add_edges_from(new_nodes_to_add)
        nodes_to_add = new_nodes_to_add

    nx.draw(G, with_labels=True)
    plt.show()


def draw_ring(num_vms):
    G = nx.cycle_graph(num_vms)
    nx.draw(G, with_labels=True)
    plt.show()

def draw_bus(num_vms):
    G = nx.path_graph(num_vms)
    nx.draw(G, with_labels=True)
    plt.show()

def draw_topology(topology, num_vms):
    if topology == 'Lineal':
        draw_linear(num_vms)
    elif topology == 'Malla':
        draw_mesh(num_vms)
    elif topology == 'Árbol':
        draw_custom_tree(num_vms)
    elif topology == 'Anillo':
        draw_ring(num_vms)
    elif topology == 'Bus':
        draw_bus(num_vms)
