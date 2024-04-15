import tkinter as tk
from tkinter import messagebox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def Johnson():

    # Draw the initial graph with edge labels
    plt.title(f"initial graph")
    pos = nx.spring_layout(graph, k=5)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='black')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='red')

    plt.show()

    # Add a new node to the graph with zero-weight edges to all other nodes
    new_node = max(graph.nodes) + 1
    graph.add_node(new_node)
    for node in graph.nodes:
        graph.add_edge(new_node, node, weight=0)

    # Run Bellman-Ford algorithm to find the shortest path from the new node to all other nodes
    distances, _ = nx.single_source_bellman_ford(graph, new_node)
    if any(np.isinf(list(distances.values()))):
        print("Graph contains a negative weight cycle")
    else:
        # Recalculate edge weights using the new node's distance to each node
        for u, v, weight in graph.edges.data('weight'):
            graph[u][v]['weight'] += distances[u] - distances[v]

        graph.remove_node(new_node)

        # Find the shortest path to all other nodes using Dijkstra's algorithm
        shortest_paths = {}
        for node in graph.nodes:
            shortest_path = nx.single_source_dijkstra_path(graph, node)
            #del(shortest_path[node])
            shortest_paths[node] = shortest_path
            print(node,' => ',shortest_paths[node])

        # reset edge weights to their initial values
        for u, v, weight in graph.edges.data('weight'):
            graph[u][v]['weight'] += distances[v] - distances[u]

        # create temporary graph G and draw a shortest path graph in each iteration
        for node in graph.nodes:
            G = nx.DiGraph()
            G.add_nodes_from(graph.nodes)
            for n in shortest_paths[node]:
                if(len(shortest_paths[node][n]) >= 2):
                    for i in range(len(shortest_paths[node][n])-1):
                        u = shortest_paths[node][n][i]
                        v = shortest_paths[node][n][i+1]
                        if((u, v) not in G.edges):
                            G.add_weighted_edges_from([(u,v,graph[u][v]['weight']),])
            print(G.nodes)
            print(G.edges)

            plt.title(f"shortest path from node {node} to other nodes")
            pos = nx.spring_layout(G, k=5)
            nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='black')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
        
            plt.show()
            del(G)



class initiate_edges:
    def __init__(self):

        root = tk.Tk()
        self.master = root
        self.master.title("Insert Edges")

        self.insert_edge_button = tk.Button(self.master, text="insert new edge",
                                               command= lambda: [self.insert_edge_button.destroy(),
                                                                 self.insert_edge(i=0)])
        self.insert_edge_button.pack()

        root.mainloop()

    def insert_edge(self, i):

        self.from_label = tk.Label(self.master, text="from(integer only):")
        self.from_entry = tk.Entry(self.master)

        self.to_label = tk.Label(self.master, text="to(integer only):")
        self.to_entry = tk.Entry(self.master)

        self.weight_label = tk.Label(self.master, text="weight(numeric):")
        self.weight_entry = tk.Entry(self.master)

        self.from_label.grid(row=0+i ,column=0)
        self.from_entry.grid(row=1+i ,column=0)
        self.to_label.grid(row=0+i ,column=1)
        self.to_entry.grid(row=1+i ,column=1)
        self.weight_label.grid(row=0+i ,column=2)
        self.weight_entry.grid(row=1+i ,column=2)

        
        self.insert_edge_button = tk.Button(self.master, text="insert new edge",
                                               command= lambda: [graph.add_edge(int(self.from_entry.get()),
                                                                                 int(self.to_entry.get()),
                                                                                 weight=float(self.weight_entry.get())), 
                                                                 self.insert_edge_button.destroy(),
                                                                 self.submit_button.destroy(),
                                                                 self.insert_edge(i+5)])
        self.insert_edge_button.grid(row=2+i, column=1)

        self.submit_button = tk.Button(self.master, text="submit",
                                               command= lambda: [graph.add_edge(int(self.from_entry.get()),
                                                                                 int(self.to_entry.get()),
                                                                                 weight=float(self.weight_entry.get())),
                                                                 print(graph.edges.data),
                                                                 self.master.destroy(),
                                                                 Johnson()])
        self.submit_button.grid(row=3+i, column=1)


class initiate_vertices:
    def __init__(self, master):
        self.master = master
        master.title("Insert Vertices")

        self.insert_vertice_button = tk.Button(master, text="insert new vertice",
                                               command= lambda: [self.insert_vertice_button.destroy(),
                                                                 self.insert_vertice()])
        self.insert_vertice_button.pack()


    def insert_vertice(self):

        self.vertice_label = tk.Label(self.master, text="insert vertice name(integer only):")
        self.vertice_label.pack()
        self.vertice_entry = tk.Entry(self.master)
        self.vertice_entry.pack()

        self.insert_vertice_button = tk.Button(self.master, text="insert new vertice",
                                                    command= lambda: [graph.add_node(int(self.vertice_entry.get())),
                                                                      self.insert_vertice_button.destroy(),
                                                                      self.submit_button.destroy() ,
                                                                      self.insert_vertice()])
        self.insert_vertice_button.pack()


        self.submit_button = tk.Button(self.master, text="submit",
                                        command= lambda: [graph.add_node(int(self.vertice_entry.get())),
                                                          print(graph.nodes),
                                                          self.master.destroy(),
                                                          initiate_edges()])
        self.submit_button.pack()

        



root = tk.Tk()
global graph
graph = nx.DiGraph()
app = initiate_vertices(root)
root.mainloop()

