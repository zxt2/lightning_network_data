import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections

PG_SQL_LOCAL = {
    'database': 'lndata',
    'user': 'postgres',
    'password': "postgres",
    'host': 'localhost',
    'port': "5432",
}


def Graph_Construct(operation, graph):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(operation)
    while True:
        rows = cursor.fetchmany(2000)
        if not rows:
            break
        for row in rows:
            satoshis, nodes, opentime = row
            graph.add_nodes_from(nodes)
            graph.add_edge(nodes[0], nodes[1], weight=satoshis, existtime=1595388849 - opentime)
    conn.close()


if __name__ == '__main__':
    G = nx.MultiGraph()
    # exist now
    operation = "select satoshis,nodes,(open :: json ->'time') from public.channels where ( close :: json -> 'time' ):: TEXT like 'null' "
    Graph_Construct(operation, G)
    G0 = nx.Graph(G)

    # metrics calculation #
    
    print('node count:', G.number_of_nodes())
    print('channel count:', G.number_of_edges())
    print('total capacity:', G.size(weight='weight'))
    degree = []
    for key, value in nx.degree(G):
        degree.append(value)
    print('average degree:', np.mean(degree))
    print('density:', nx.density(G))

    print('average clustering coefficient:', nx.average_clustering(G0))
    print('transitivity:', nx.transitivity(G0))
    print('degree assortativity:', nx.degree_assortativity_coefficient(G0))

    # Maximum Connected Components --> MCC
    MCC = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)
    print('nodes of the maximum connected components:', MCC.number_of_nodes())
    print('channels of the maximum connected components:',MCC.number_of_edges())
    print('diameter of the maximum connected components:', nx.diameter(MCC))
    print('average shortest path length in the MCC:', nx.average_shortest_path_length(MCC))
    
    # results of connected components
    capacity_7544 = []
    capacity_5 = []
    capacity_3 = []
    capacity_2 = []
    existtime_7544 = []
    existtime_5 = []
    existtime_3 = []
    existtime_2 = []
    for c in nx.connected_components(G):
        if len(c) == 7544:
            CC = G.subgraph(c)
            for u, v, data in CC.edges(data=True):
                capacity_7544.append(data['weight'])
                existtime_7544.append(data['existtime'])
        if len(c) == 5:
            CC = G.subgraph(c)
            for u, v, data in CC.edges(data=True):
                capacity_5.append(data['weight'])
                existtime_5.append(data['existtime'])
        if len(c) == 3:
            CC = G.subgraph(c)
            for u, v, data in CC.edges(data=True):
                capacity_3.append(data['weight'])
                existtime_3.append(data['existtime'])
        if len(c) == 2:
            CC = G.subgraph(c)
            for u, v, data in CC.edges(data=True):
                capacity_2.append(data['weight'])
                existtime_2.append(data['existtime'])
    print('average channel capacity of 7544:', np.mean(capacity_7544))
    print('average channel capacity of 5:', np.mean(capacity_5))
    print('average channel capacity of 3:', np.mean(capacity_3))
    print('average channel capacity of 2:', np.mean(capacity_2))
    print('average channel existtime of 7544:', np.mean(existtime_7544)/86400)
    print('average channel existtime of 5:', np.mean(existtime_5)/86400)
    print('average channel existtime of 3:', np.mean(existtime_3)/86400)
    print('average channel existtime of 2:', np.mean(existtime_2)/86400)
    

    # average shortest path length of big nodes/channels in the MCC
    MCC = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)
    bignode_nodes = []
    bigchannel_nodes = []
    
    for key, value in MCC.degree(weight='weight'):
        if value >= 10000000:
            bignode_nodes.append(key)
    
    for u, v, data in MCC.edges(data=True):
        if data['weight'] >= 10000000:
            bigchannel_nodes.append(u)
            bigchannel_nodes.append(v)
    
    sum_bignodes = 0
    sum_bigchannels = 0
    average_bignodes = 0
    average_bigchannels = 0
    
	for i in bignode_nodes:
        for j in bignode_nodes:
            sum_bignodes += nx.shortest_path_length(MCC, source=i, target=j)
    for i in bigchannel_nodes:
        for j in bigchannel_nodes:
            sum_bigchannels += nx.shortest_path_length(MCC, source=i, target=j)
    
    print(sum_bignodes)
    print(sum_bigchannels)
    average_bignodes=sum_bignodes/(len(bignode_nodes)*(len(bignode_nodes)-1))
    average_bigchannels = sum_bigchannels / (len(bigchannel_nodes) * (len(bigchannel_nodes) - 1))
    print('average shortest path length of big nodes in the MCC:', average_bignodes)
    print('average shortest path length of big channels in the MCC:', average_bigchannels)
  

    
    # metrics comparisons with similar scale networks
    # regular graph
    RG = nx.random_graphs.random_regular_graph(10, 7647)
    print(RG.number_of_edges())
    degree = []
    for key, value in nx.degree(RG):
        degree.append(value)
    print('average degree:', np.mean(degree))
    print('density:', nx.density(RG))

    print('average clustering coefficient:', nx.average_clustering(RG))
    print('transitivity:', nx.transitivity(RG))
    print('degree assortativity:', nx.degree_assortativity_coefficient(RG))
    # ER graph
    ER = nx.random_graphs.erdos_renyi_graph(7647, 0.00133)
    print(ER.number_of_edges())
    degree = []
    for key, value in nx.degree(ER):
        degree.append(value)
    print('average degree:', np.mean(degree))
    print('density:', nx.density(ER))

    print('average clustering coefficient:', nx.average_clustering(ER))
    print('transitivity:', nx.transitivity(ER))
    print('degree assortativity:', nx.degree_assortativity_coefficient(ER))
    # WS network
    WS = nx.random_graphs.watts_strogatz_graph(7647, 10, 0.3)
    print(WS.number_of_edges())
    degree = []
    for key, value in nx.degree(WS):
        degree.append(value)
    print('average degree:', np.mean(degree))
    print('density:', nx.density(WS))

    print('average clustering coefficient:', nx.average_clustering(WS))
    print('transitivity:', nx.transitivity(WS))
    print('degree assortativity:', nx.degree_assortativity_coefficient(WS))
    # BA network
    BA = nx.random_graphs.barabasi_albert_graph(7647, 5)
    print(BA.number_of_edges())
    degree = []
    for key, value in nx.degree(BA):
        degree.append(value)
    print('average degree:', np.mean(degree))
    print('density:', nx.density(BA))

    print('average clustering coefficient:', nx.average_clustering(BA))
    print('transitivity:', nx.transitivity(BA))
    print('degree assortativity:', nx.degree_assortativity_coefficient(BA))
    
