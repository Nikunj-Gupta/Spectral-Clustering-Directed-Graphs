import pandas as pd, numpy as np, matplotlib.pyplot as plt, networkx as nx

def get_graph(data, colsX="pickup_community_area", colsY='dropoff_community_area', weights='num_trips', head=True): 
    if weights == 'num_trips': 
        ## Adjacency Matrix (Directed Graph)
        ## pickup vs dropoff : number of trips (one way) 
        df = pd.crosstab(data[colsX], data[colsY])
        idx = df.columns.union(df.index)
        df = df.reindex(index = idx, columns=idx, fill_value=0) 
        
    ## Directed Graph 
    if head: G_di = nx.from_pandas_adjacency(df.head(), create_using=nx.DiGraph) 
    else: G_di = nx.from_pandas_adjacency(df, create_using=nx.DiGraph) 
    
    ## Undirected Graph 
    ## pickup vs dropoff : number of trips (to and fro) 

    G_un = nx.Graph()
    G_un.add_edges_from(G_di.edges(), weight=0) 
    for u, v, d in G_di.edges(data=True):
        G_un[u][v]['weight'] += d['weight']

    A_di = nx.to_numpy_array(G_di) 
    A_un = nx.to_numpy_array(G_un) 

    return G_di, A_di, G_un, A_un 

def draw(G):
    from pylab import rcParams
    rcParams['figure.figsize'] = 14, 10

    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, node_size=2500, node_color ='green')
    labels = nx.get_edge_attributes(G, 'weight') 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels) 