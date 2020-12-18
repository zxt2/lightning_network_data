import psycopg2
import networkx as nx
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn import linear_model
import powerlaw

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
            satoshis, nodes = row
            graph.add_nodes_from(nodes)
            graph.add_edge(nodes[0], nodes[1], weight=satoshis)
    conn.close()


def average_degree(g_degree):
    degree = []
    for key, value in g_degree:
        degree.append(value)
    return np.mean(degree)


def degree_distribution_fitting(graph):
    degree = []
    for node in graph.nodes():
        degree.append(graph.degree(node))

    data = degree
    fit = powerlaw.Fit(data, discrete=True)
    print(fit.power_law.alpha)
    return fit.power_law.alpha


def monthly_nodes_edges():
    monthly_nodes = []
    monthly_edges = []
    monthly_total_capacity = []
    monthly_nodes_average_degree = []
    monthly_density = []
    monthly_alpha = []

    # 2018-02-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1517414400) ) and ((open ->>'time')::text::integer <= 1517414400)"
    Graph_Construct(operation, G1)
    monthly_nodes.append(G1.number_of_nodes())
    monthly_edges.append(G1.number_of_edges())
    monthly_total_capacity.append(G1.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G1)))
    monthly_density.append(nx.density(G1))

    print('2018-02-01')
    monthly_alpha.append(degree_distribution_fitting(G1))

    # 2018-03-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1519833600) ) and ((open ->>'time')::text::integer <= 1519833600)"
    Graph_Construct(operation, G2)
    monthly_nodes.append(G2.number_of_nodes())
    monthly_edges.append(G2.number_of_edges())
    monthly_total_capacity.append(G2.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G2)))
    monthly_density.append(nx.density(G2))

    print('2018-03-01')
    monthly_alpha.append(degree_distribution_fitting(G2))

    # 2018-04-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1522512000) ) and ((open ->>'time')::text::integer <= 1522512000)"
    Graph_Construct(operation, G3)
    monthly_nodes.append(G3.number_of_nodes())
    monthly_edges.append(G3.number_of_edges())
    monthly_total_capacity.append(G3.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G3)))
    monthly_density.append(nx.density(G3))

    print('2018-04-01')
    monthly_alpha.append(degree_distribution_fitting(G3))

    # 2018-05-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1525104000) ) and ((open ->>'time')::text::integer <= 1525104000)"
    Graph_Construct(operation, G4)
    monthly_nodes.append(G4.number_of_nodes())
    monthly_edges.append(G4.number_of_edges())
    monthly_total_capacity.append(G4.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G4)))
    monthly_density.append(nx.density(G4))

    print('2018-05-01')
    monthly_alpha.append(degree_distribution_fitting(G4))

    # 2018-06-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1527782400) ) and ((open ->>'time')::text::integer <= 1527782400)"
    Graph_Construct(operation, G5)
    monthly_nodes.append(G5.number_of_nodes())
    monthly_edges.append(G5.number_of_edges())
    monthly_total_capacity.append(G5.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G5)))
    monthly_density.append(nx.density(G5))

    print('2018-06-01')
    monthly_alpha.append(degree_distribution_fitting(G5))

    # 2018-07-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1530374400) ) and ((open ->>'time')::text::integer <= 1530374400)"
    Graph_Construct(operation, G6)
    monthly_nodes.append(G6.number_of_nodes())
    monthly_edges.append(G6.number_of_edges())
    monthly_total_capacity.append(G6.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G6)))
    monthly_density.append(nx.density(G6))

    print('2018-07-01')
    monthly_alpha.append(degree_distribution_fitting(G6))

    # 2018-08-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1533052800) ) and ((open ->>'time')::text::integer <= 1533052800)"
    Graph_Construct(operation, G7)
    monthly_nodes.append(G7.number_of_nodes())
    monthly_edges.append(G7.number_of_edges())
    monthly_total_capacity.append(G7.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G7)))
    monthly_density.append(nx.density(G7))

    print('2018-08-01')
    monthly_alpha.append(degree_distribution_fitting(G7))

    # 2018-09-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1535731200) ) and ((open ->>'time')::text::integer <= 1535731200)"
    Graph_Construct(operation, G8)
    monthly_nodes.append(G8.number_of_nodes())
    monthly_edges.append(G8.number_of_edges())
    monthly_total_capacity.append(G8.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G8)))
    monthly_density.append(nx.density(G8))

    print('2018-09-01')
    monthly_alpha.append(degree_distribution_fitting(G8))

    # 2018-10-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1538323200) ) and ((open ->>'time')::text::integer <= 1538323200)"
    Graph_Construct(operation, G9)
    monthly_nodes.append(G9.number_of_nodes())
    monthly_edges.append(G9.number_of_edges())
    monthly_total_capacity.append(G9.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G9)))
    monthly_density.append(nx.density(G9))
	
    print('2018-10-01')
    monthly_alpha.append(degree_distribution_fitting(G9))

    # 2018-11-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1541001600) ) and ((open ->>'time')::text::integer <= 1541001600)"
    Graph_Construct(operation, G10)
    monthly_nodes.append(G10.number_of_nodes())
    monthly_edges.append(G10.number_of_edges())
    monthly_total_capacity.append(G10.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G10)))
    monthly_density.append(nx.density(G10))

    print('2018-11-01')
    monthly_alpha.append(degree_distribution_fitting(G10))

    # 2018-12-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1543593600) ) and ((open ->>'time')::text::integer <= 1543593600)"
    Graph_Construct(operation, G11)
    monthly_nodes.append(G11.number_of_nodes())
    monthly_edges.append(G11.number_of_edges())
    monthly_total_capacity.append(G11.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G11)))
    monthly_density.append(nx.density(G11))

    print('2018-12-01')
    monthly_alpha.append(degree_distribution_fitting(G11))

    # 2019-01-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1546272000) ) and ((open ->>'time')::text::integer <= 1546272000)"
    Graph_Construct(operation, G12)
    monthly_nodes.append(G12.number_of_nodes())
    monthly_edges.append(G12.number_of_edges())
    monthly_total_capacity.append(G12.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G12)))
    monthly_density.append(nx.density(G12))

    print('2019-01-01')
    monthly_alpha.append(degree_distribution_fitting(G12))

    # 2019-02-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1548950400) ) and ((open ->>'time')::text::integer <= 1548950400)"
    Graph_Construct(operation, G13)
    monthly_nodes.append(G13.number_of_nodes())
    monthly_edges.append(G13.number_of_edges())
    monthly_total_capacity.append(G13.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G13)))
    monthly_density.append(nx.density(G13))

    print('2019-02-01')
    monthly_alpha.append(degree_distribution_fitting(G13))

    # 2019-03-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1551369600) ) and ((open ->>'time')::text::integer <= 1551369600)"
    Graph_Construct(operation, G14)
    monthly_nodes.append(G14.number_of_nodes())
    monthly_edges.append(G14.number_of_edges())
    monthly_total_capacity.append(G14.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G14)))
    monthly_density.append(nx.density(G14))

    print('2019-03-01')
    monthly_alpha.append(degree_distribution_fitting(G14))

    # 2019-04-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1554048000) ) and ((open ->>'time')::text::integer <= 1554048000)"
    Graph_Construct(operation, G15)
    monthly_nodes.append(G15.number_of_nodes())
    monthly_edges.append(G15.number_of_edges())
    monthly_total_capacity.append(G15.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G15)))
    monthly_density.append(nx.density(G15))

    print('2019-04-01')
    monthly_alpha.append(degree_distribution_fitting(G15))

    # 2019-05-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1556640000) ) and ((open ->>'time')::text::integer <= 1556640000)"
    Graph_Construct(operation, G16)
    monthly_nodes.append(G16.number_of_nodes())
    monthly_edges.append(G16.number_of_edges())
    monthly_total_capacity.append(G16.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G16)))
    monthly_density.append(nx.density(G16))

    print('2019-05-01')
    monthly_alpha.append(degree_distribution_fitting(G16))

    # 2019-06-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1559318400) ) and ((open ->>'time')::text::integer <= 1559318400)"
    Graph_Construct(operation, G17)
    monthly_nodes.append(G17.number_of_nodes())
    monthly_edges.append(G17.number_of_edges())
    monthly_total_capacity.append(G17.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G17)))
    monthly_density.append(nx.density(G17))

    print('2019-06-01')
    monthly_alpha.append(degree_distribution_fitting(G17))

    # 2019-07-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1561910400) ) and ((open ->>'time')::text::integer <= 1561910400)"
    Graph_Construct(operation, G18)
    monthly_nodes.append(G18.number_of_nodes())
    monthly_edges.append(G18.number_of_edges())
    monthly_total_capacity.append(G18.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G18)))
    monthly_density.append(nx.density(G18))

    print('2019-07-01')
    monthly_alpha.append(degree_distribution_fitting(G18))

    # 2019-08-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1564588800) ) and ((open ->>'time')::text::integer <= 1564588800)"
    Graph_Construct(operation, G19)
    monthly_nodes.append(G19.number_of_nodes())
    monthly_edges.append(G19.number_of_edges())
    monthly_total_capacity.append(G19.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G19)))
    monthly_density.append(nx.density(G19))

    print('2019-08-01')
    monthly_alpha.append(degree_distribution_fitting(G19))

    # 2019-09-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1567267200) ) and ((open ->>'time')::text::integer <= 1567267200)"
    Graph_Construct(operation, G20)
    monthly_nodes.append(G20.number_of_nodes())
    monthly_edges.append(G20.number_of_edges())
    monthly_total_capacity.append(G20.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G20)))
    monthly_density.append(nx.density(G20))

    print('2019-09-01')
    monthly_alpha.append(degree_distribution_fitting(G20))

    # 2019-10-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1569859200) ) and ((open ->>'time')::text::integer <= 1569859200)"
    Graph_Construct(operation, G21)
    monthly_nodes.append(G21.number_of_nodes())
    monthly_edges.append(G21.number_of_edges())
    monthly_total_capacity.append(G21.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G21)))
    monthly_density.append(nx.density(G21))

    print('2019-10-01')
    monthly_alpha.append(degree_distribution_fitting(G21))

    # 2019-11-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1572537600) ) and ((open ->>'time')::text::integer <= 1572537600)"
    Graph_Construct(operation, G22)
    monthly_nodes.append(G22.number_of_nodes())
    monthly_edges.append(G22.number_of_edges())
    monthly_total_capacity.append(G22.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G22)))
    monthly_density.append(nx.density(G22))

    print('2019-11-01')
    monthly_alpha.append(degree_distribution_fitting(G22))

    # 2019-12-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1575129600) ) and ((open ->>'time')::text::integer <= 1575129600)"
    Graph_Construct(operation, G23)
    monthly_nodes.append(G23.number_of_nodes())
    monthly_edges.append(G23.number_of_edges())
    monthly_total_capacity.append(G23.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G23)))
    monthly_density.append(nx.density(G23))

    print('2019-12-01')
    monthly_alpha.append(degree_distribution_fitting(G23))

    # 2020-01-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1577808000) ) and ((open ->>'time')::text::integer <= 1577808000)"
    Graph_Construct(operation, G24)
    monthly_nodes.append(G24.number_of_nodes())
    monthly_edges.append(G24.number_of_edges())
    monthly_total_capacity.append(G24.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G24)))
    monthly_density.append(nx.density(G24))

    print('2020-01-01')
    monthly_alpha.append(degree_distribution_fitting(G24))

    # 2020-02-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1580486400) ) and ((open ->>'time')::text::integer <= 1580486400)"
    Graph_Construct(operation, G25)
    monthly_nodes.append(G25.number_of_nodes())
    monthly_edges.append(G25.number_of_edges())
    monthly_total_capacity.append(G25.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G25)))
    monthly_density.append(nx.density(G25))

    print('2020-02-01')
    monthly_alpha.append(degree_distribution_fitting(G25))

    # 2020-03-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1582992000) ) and ((open ->>'time')::text::integer <= 1582992000)"
    Graph_Construct(operation, G26)
    monthly_nodes.append(G26.number_of_nodes())
    monthly_edges.append(G26.number_of_edges())
    monthly_total_capacity.append(G26.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G26)))
    monthly_density.append(nx.density(G26))

    print('2020-03-01')
    monthly_alpha.append(degree_distribution_fitting(G26))

    # 2020-04-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1585670400) ) and ((open ->>'time')::text::integer <= 1585670400)"
    Graph_Construct(operation, G27)
    monthly_nodes.append(G27.number_of_nodes())
    monthly_edges.append(G27.number_of_edges())
    monthly_total_capacity.append(G27.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G27)))
    monthly_density.append(nx.density(G27))

    print('2020-04-01')
    monthly_alpha.append(degree_distribution_fitting(G27))

    # 2020-05-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1588262400) ) and ((open ->>'time')::text::integer <= 1588262400)"
    Graph_Construct(operation, G28)
    monthly_nodes.append(G28.number_of_nodes())
    monthly_edges.append(G28.number_of_edges())
    monthly_total_capacity.append(G28.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G28)))
    monthly_density.append(nx.density(G28))

    print('2020-05-01')
    monthly_alpha.append(degree_distribution_fitting(G28))

    # 2020-06-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1590940800) ) and ((open ->>'time')::text::integer <= 1590940800)"
    Graph_Construct(operation, G29)
    monthly_nodes.append(G29.number_of_nodes())
    monthly_edges.append(G29.number_of_edges())
    monthly_total_capacity.append(G29.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G29)))
    monthly_density.append(nx.density(G29))

    print('2020-06-01')
    monthly_alpha.append(degree_distribution_fitting(G29))

    # 2020-07-01
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1593532800) ) and ((open ->>'time')::text::integer <= 1593532800)"
    Graph_Construct(operation, G30)
    monthly_nodes.append(G30.number_of_nodes())
    monthly_edges.append(G30.number_of_edges())
    monthly_total_capacity.append(G30.size(weight='weight'))
    monthly_nodes_average_degree.append(average_degree(nx.degree(G30)))
    monthly_density.append(nx.density(G30))

    print('2020-07-01')
    monthly_alpha.append(degree_distribution_fitting(G30))

    return monthly_nodes, monthly_edges, monthly_total_capacity, monthly_nodes_average_degree, monthly_density, monthly_alpha


if __name__ == '__main__':
    # monthly snapshots from 2018-02-01 00:00:00 to 2020-07-01 00:00:00 (30 months)
    # network graph of each month
    G1 = nx.MultiGraph()
    G2 = nx.MultiGraph()
    G3 = nx.MultiGraph()
    G4 = nx.MultiGraph()
    G5 = nx.MultiGraph()
    G6 = nx.MultiGraph()
    G7 = nx.MultiGraph()
    G8 = nx.MultiGraph()
    G9 = nx.MultiGraph()
    G10 = nx.MultiGraph()
    G11 = nx.MultiGraph()
    G12 = nx.MultiGraph()
    G13 = nx.MultiGraph()
    G14 = nx.MultiGraph()
    G15 = nx.MultiGraph()
    G16 = nx.MultiGraph()
    G17 = nx.MultiGraph()
    G18 = nx.MultiGraph()
    G19 = nx.MultiGraph()
    G20 = nx.MultiGraph()
    G21 = nx.MultiGraph()
    G22 = nx.MultiGraph()
    G23 = nx.MultiGraph()
    G24 = nx.MultiGraph()
    G25 = nx.MultiGraph()
    G26 = nx.MultiGraph()
    G27 = nx.MultiGraph()
    G28 = nx.MultiGraph()
    G29 = nx.MultiGraph()
    G30 = nx.MultiGraph()

    monthly_nodes, monthly_edges, monthly_total_capacity, monthly_nodes_average_degree, monthly_density, monthly_alpha = monthly_nodes_edges()
    monthly_edges_average_capacity = np.array(monthly_total_capacity) / np.array(monthly_edges)
    monthly_nodes_average_capacity = np.array(monthly_total_capacity) / np.array(monthly_nodes)

    monthly_data = {}
    for i in monthly_nodes:
        monthly_data.setdefault('monthly_nodes', []).append(i)
    for j in monthly_edges:
        monthly_data.setdefault('monthly_edges', []).append(j)
    for k in monthly_total_capacity:
        monthly_data.setdefault('monthly_total_capacity', []).append(k)
    for l in monthly_edges_average_capacity:
        monthly_data.setdefault('monthly_edges_average_capacity', []).append(l)
    for m in monthly_nodes_average_degree:
        monthly_data.setdefault('monthly_nodes_average_degree', []).append(m)
    for n in monthly_nodes_average_capacity:
        monthly_data.setdefault('monthly_nodes_average_capacity', []).append(n)
    for o in monthly_density:
        monthly_data.setdefault('monthly_density', []).append(o)
    for p in monthly_alpha:
        monthly_data.setdefault('monthly_alpha', []).append(p)

    filename = 'monthly_data.json'
    with open(filename, 'w') as file_obj:
        json.dump(monthly_data, file_obj)
