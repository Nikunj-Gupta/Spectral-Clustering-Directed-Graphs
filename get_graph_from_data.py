import pandas as pd, numpy as np, matplotlib.pyplot as plt, networkx as nx

def get_graph(data, colsX="pickup_community_area", colsY='dropoff_community_area', weights='num_trips', head=True): 
    if weights == 'num_trips': 
        ## Adjacency Matrix (Directed Graph)
        ## pickup vs dropoff : number of trips (one way) 
        # df = pd.crosstab(data[colsX], data[colsY])
        # idx = df.columns.union(df.index)
        # df = df.reindex(index = idx, columns=idx, fill_value=0) 
        
        df = pd.crosstab(index=data.pickup_community_area, 
                    columns=data.dropoff_community_area, 
                    values=data.trip_seconds,
                    aggfunc=np.mean).round(2).fillna(0) 
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

def draw(G, clusters=None):
    from pylab import rcParams
    rcParams['figure.figsize'] = 24, 24 



    # pos = nx.spring_layout(G,scale=20, k=3/np.sqrt(G.order()))
    
    if clusters is not None: 
        #     colors = ["tab:red", "tab:blue", "tab:green", "tab:purple", "tab:olive", "tab:orange", "tab:cyan", "tab:pink"] 
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        mapping = [colors[i] for i in clusters] 
        nx.draw_kamada_kawai(G, node_size=2500, node_color = mapping, width=0.1, with_labels=True)
    else: 
        nx.draw_kamada_kawai(G, node_size=2500, node_color = 'green', width=0.1, with_labels=True)
    # labels = nx.get_edge_attributes(G, 'weight') 
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels) 