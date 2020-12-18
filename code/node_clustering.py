import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import operator
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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
            short_channel_id, satoshis, nodes = row
            graph.add_node(nodes[0], totalbasefee=0, totalfee=0)
            graph.add_node(nodes[1], totalbasefee=0, totalfee=0)
            graph.add_edge(nodes[0], nodes[1], id=short_channel_id, weight=satoshis)
    conn.close()


def Charge_Policy(graph):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(
        "select DISTINCT ON(policies.short_channel_id) policies.short_channel_id,channels.nodes,policies.base_fee_millisatoshi,policies.fee_per_millionth from policies,channels where policies.direction=1 and policies.short_channel_id=channels.short_channel_id and ( channels.close :: json -> 'time' ):: TEXT like 'null' order by policies.short_channel_id,policies.update_time desc")
    while True:
        rows = cursor.fetchmany(2000)
        if not rows:
            break
        for row in rows:
            short_channel_id, nodes, base_fee_millisatoshi, fee_per_millionth = row
            graph.nodes[nodes[0]]['totalbasefee'] += base_fee_millisatoshi
            graph.nodes[nodes[0]]['totalfee'] += fee_per_millionth
    conn.close()

    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(
        "select DISTINCT ON(policies.short_channel_id) policies.short_channel_id,channels.nodes,policies.base_fee_millisatoshi,policies.fee_per_millionth from policies,channels where policies.direction=0 and policies.short_channel_id=channels.short_channel_id and ( channels.close :: json -> 'time' ):: TEXT like 'null' order by policies.short_channel_id,policies.update_time desc")
    while True:
        rows = cursor.fetchmany(2000)
        if not rows:
            break
        for row in rows:
            short_channel_id, nodes, base_fee_millisatoshi, fee_per_millionth = row
            graph.nodes[nodes[1]]['totalbasefee'] += base_fee_millisatoshi
            graph.nodes[nodes[1]]['totalfee'] += fee_per_millionth
    conn.close()


def Node_Feature(graph, graph0):
    node_id2 = []
    node_id3 = []
    node_id4 = []
    node_id5 = []
    node_id6 = []
    node_id7 = []
    node_id8 = []

    node_id = []
    node_degree = []
    node_capacity = []
    clustering_coef = []
    degree_centrality = []
    closeness_centrality = []
    betweenness_centrality = []
    eigenvector_centrality = []
    basefee = []
    fee = []

    nodedegree = graph.degree()
    nodecapacity = graph.degree(weight='weight')
    clusteringcoef = nx.clustering(graph0)
    degreecentrality = nx.degree_centrality(graph)
    closenesscentrality = nx.closeness_centrality(graph)
    betweennesscentrality = nx.betweenness_centrality(graph0)
    eigenvectorcentrality = nx.eigenvector_centrality(graph0)

    for key, value in nodedegree:
        node_id.append(key)
        node_degree.append(value)
    for key, value in nodecapacity:
        node_capacity.append(value)
        node_id2.append(key)
    for key, value in clusteringcoef.items():
        clustering_coef.append(value)
        node_id3.append(key)
    for key, value in degreecentrality.items():
        degree_centrality.append(value)
        node_id4.append(key)
    for key, value in closenesscentrality.items():
        closeness_centrality.append(value)
        node_id5.append(key)
    for key, value in betweennesscentrality.items():
        betweenness_centrality.append(value)
        node_id6.append(key)
    for key, value in eigenvectorcentrality.items():
        eigenvector_centrality.append(value)
        node_id7.append(key)

    for node, data in graph.nodes(data=True):
        node_id8.append(node)
        basefee.append(data['totalbasefee'] / graph.degree(node))
        fee.append(data['totalfee'] / graph.degree(node))

    print(operator.eq(node_id, node_id2))
    print(operator.eq(node_id, node_id3))
    print(operator.eq(node_id, node_id4))
    print(operator.eq(node_id, node_id5))
    print(operator.eq(node_id, node_id6))
    print(operator.eq(node_id, node_id7))
    print(operator.eq(node_id, node_id8))

    return node_id, node_degree, node_capacity, clustering_coef, degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality, basefee, fee


if __name__ == '__main__':
    '''
    G = nx.MultiGraph()
    # exist now
    operation = "select short_channel_id,satoshis,nodes from public.channels where ( close :: json -> 'time' ):: TEXT like 'null' "
    Graph_Construct(operation, G)
    Charge_Policy(G)
    G0 = nx.Graph(G)

    # gain various node data
    node_id, node_degree, node_capacity, clustering_coef, degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality, basefee, fee = Node_Feature(
        G, G0)
    node_dict = {
        'node_id': node_id,
        'node_degree': node_degree,
        'node_capacity': node_capacity,
        'clustering_coef': clustering_coef,
        'degree_centrality': degree_centrality,
        'closeness_centrality': closeness_centrality,
        'betweenness_centrality': betweenness_centrality,
        'eigenvector_centrality': eigenvector_centrality,
        'base_fee_millisatoshi': basefee,
        'fee_per_millionth': fee
    }
    node_data = pd.DataFrame(data=node_dict)
    node_data.to_excel('node_data.xlsx')
    '''

    # select node features
    data = pd.DataFrame(pd.read_excel('node_data.xlsx'))
    features = ['node_degree', 'node_capacity', 'clustering_coef', 'degree_centrality', 'closeness_centrality',
                'betweenness_centrality', 'eigenvector_centrality', 'base_fee_millisatoshi', 'fee_per_millionth']
    # print(data[features])

    # K-means
    km = KMeans(n_clusters=4)
    km = km.fit(data[features])
    labels = km.predict(data[features])
    # result
    r1 = pd.Series(km.labels_).value_counts()
    r2 = pd.DataFrame(km.cluster_centers_)
    r = pd.concat([r2, r1], axis=1)
    r.columns = features + [u'count']
    r.to_excel('result.xlsx')

    # evaluation
    print("Silhouette Coefficient:",metrics.silhouette_score(data[features], labels, metric='euclidean'))
    print("Calinski Harabasz Score:",metrics.calinski_harabasz_score(data[features],labels))
    print("DBI:",metrics.davies_bouldin_score(data[features],labels))
	