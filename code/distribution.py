import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections
import statsmodels.api as sm
import powerlaw
import scipy.special
import pandas as pd
import seaborn as sns

from matplotlib import cm
from matplotlib import rcParams


PG_SQL_LOCAL = {
    'database': 'lndata',
    'user': 'postgres',
    'password': "postgres",
    'host': 'localhost',
    'port': "5432",
}

font_size = 45

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


def Graph_Construct_closedchannels(operation, graph):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(operation)
    while True:
        rows = cursor.fetchmany(2000)
        if not rows:
            break
        for row in rows:
            satoshis, nodes, opentime, closetime = row
            graph.add_nodes_from(nodes)
            graph.add_edge(nodes[0], nodes[1], weight=satoshis, existtime=int(closetime) - opentime)
    conn.close()


def node_capacity_distribution(graph):
    # get node capacity
    node_capacity = graph.degree(weight='weight')
    # for key, value in node_capacity:
    # if value == 8426751147:
    # print(key)  # node ACINQ
    nodecapacity = []
    for key, value in node_capacity:
        nodecapacity.append(value)

    # CDF
    ecdf = sm.distributions.ECDF(nodecapacity)
    x = np.linspace(min(nodecapacity), max(nodecapacity))
    y = ecdf(x)

    plt.clf()
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = 'Times New Roman'
    rcParams['mathtext.fontset'] = 'stix'
    plt.figure(figsize=(10, 10))
    plt.step(x, y, linewidth=4, color='#3366CC')
    plt.xlim(10 ** 2, 10 ** 10)
    plt.ylim(0, 1.1)
    plt.xscale('log')
    plt.xlabel("node capacity (sat)", fontsize=font_size)
    plt.ylabel("CDF", fontsize=font_size)
    plt.tick_params(labelsize=font_size)
    plt.grid()
    plt.savefig('Current Network\\node_capacity_distribution.png', format='PNG', bbox_inches='tight')

    # big node capacity
    bignodes = []
    for cap in nodecapacity:
        if cap >= 10000000:
            bignodes.append(cap)
    # print('number of big nodes:', len(bignodes))
    # print('total capacity of big nodes:', sum(bignodes))

    # histogram
    nc_sequence = sorted([d for d in bignodes], reverse=True)
    nc_count = collections.Counter(nc_sequence)
    cap, cnt = zip(*nc_count.items())

    cBTC_cap = []
    for k in cap:
        cBTC_cap.append(k / 1000000)

    norm = plt.Normalize(0, 32)
    norm_values = norm(cnt)
    map_vir = cm.get_cmap(name='Blues_r')
    colors = map_vir(norm_values)

    plt.clf()
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = 'Times New Roman'
    rcParams['mathtext.fontset'] = 'stix'
    plt.figure(figsize=(10, 10))
    plt.bar(cBTC_cap, cnt, alpha=0.8, width=0.8, color=colors)
    #plt.xlim(10 ** 0, 10 ** 4)
    plt.ylim(0, 16)
    plt.yticks([0,4,8,12,16])
    plt.xscale('log')
    plt.xlabel("node capacity (${10^{-2}}$BTC)", fontsize=font_size)
    plt.ylabel("number of nodes", fontsize=font_size)
    plt.tick_params(labelsize=font_size)
    plt.grid()
    plt.savefig('Current Network\\big_node_capacity_distribution.png', format='PNG', bbox_inches='tight')


def channel_capacity_distribution(G):
    # get channel capacity
    channelcapacity = []
    # existtime = []
    for u, v, data in G.edges(data=True):
        channelcapacity.append(data['weight'])
        # existtime.append(data['existtime'])
    # print('average existtime(days) of all channels:', np.mean(existtime) / 86400)

    # CDF
    ecdf = sm.distributions.ECDF(channelcapacity)
    x = np.linspace(min(channelcapacity), max(channelcapacity))
    y = ecdf(x)

    plt.clf()
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = 'Times New Roman'
    rcParams['mathtext.fontset'] = 'stix'
    plt.figure(figsize=(10, 10))
    plt.step(x, y, linewidth=4, color='#660099')
    plt.xlim(10 ** 2, 10 ** 9)
    plt.ylim(0, 1.1)
    plt.xscale('log')
    plt.xlabel("channel capacity (sat)", fontsize=font_size)
    plt.ylabel("CDF", fontsize=font_size)
    plt.tick_params(labelsize=font_size)
    plt.grid()
    plt.savefig('Current Network\\channel_capacity_distribution.png', format='PNG', bbox_inches='tight')

    # big channel capacity
    bigchannels = []
    # bigchannels_existtime = []
    for u, v, data in G.edges(data=True):
        if data['weight'] >= 10000000:
            bigchannels.append(data['weight'])
            # bigchannels_existtime.append(data['existtime'])
    # print('number of big channels:', len(bigchannels))
    # print('total capacity of big channels:', sum(bigchannels))
    # print('average existtime(days) of big channels:', np.mean(bigchannels_existtime) / 86400)

    # histogram
    cc_sequence = sorted([d for d in bigchannels], reverse=True)
    cc_count = collections.Counter(cc_sequence)
    cap, cnt = zip(*cc_count.items())

    cBTC_cap = []
    for k in cap:
        cBTC_cap.append(k / 1000000)

    norm = plt.Normalize(0, 3200)
    norm_values = norm(cnt)
    map_vir = cm.get_cmap(name='Purples_r')
    colors = map_vir(norm_values)

    plt.clf()
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = 'Times New Roman'
    rcParams['mathtext.fontset'] = 'stix'
    plt.figure(figsize=(10, 10))
    plt.bar(cBTC_cap, cnt, alpha=0.8, width=0.8, color=colors)
    #plt.xlim(10 ** 0, 10 ** 3)
    plt.ylim(0, 1600)
    plt.xscale('log')
    plt.xlabel("channel capacity (${10^{-2}}$BTC)", fontsize=font_size)
    plt.ylabel("number of channels", fontsize=font_size)
    plt.tick_params(labelsize=font_size)
    plt.grid()
    plt.savefig('Current Network\\big_channel_capacity_distribution.png', format='PNG', bbox_inches='tight')


def degree_distribution_fitting(graph):
    degree = []
    for node in graph.nodes():
        degree.append(graph.degree(node))

    data = degree
    fit = powerlaw.Fit(data, discrete=True)
    print(fit.power_law.alpha)
    print(fit.power_law.xmin)
    R, p = fit.distribution_compare('power_law', 'lognormal_positive')
    print(R, p)

    numberlist = list(set(degree))
    dict = {}
    for item in numberlist:
        dict[item] = degree.count(item)
    # calculation proportion
    totalcount = sum(list(dict.values()))
    for k, v in dict.items():
        dict[k] = v / totalcount

    plt.clf()
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = 'Times New Roman'
    rcParams['mathtext.fontset'] = 'stix'
    plt.figure(figsize=(10, 10))
    plt.scatter(list(dict.keys()), list(dict.values()), marker='x', c='#3366CC', alpha=0.8, s=40)
    plt.ylim(10 ** -4, 10 ** 0)
    plt.xlim(10 ** 0, 10 ** 4)
    #plt.xticks([10 ** 0, 10 ** 1, 10 ** 2, 10 ** 3, 10 ** 4])
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('degree', fontsize=font_size)
    plt.ylabel('proportion of nodes', fontsize=font_size)
    plt.tick_params(labelsize=font_size)
    plt.grid()

    fit.power_law.plot_pdf(linestyle='--', linewidth='3', c='k')
    plt.text(10 ** 1.6, 10 ** -1.5, "$y\sim x^{%.2f}$" % (-fit.power_law.alpha), size=55)
    plt.savefig('Current Network\\degree_distribution.png', format='PNG', bbox_inches='tight')


def clustering_coefficient_distribution(graph):
    # get clustering coefficient
    clustering_coefficient = nx.clustering(graph).values()

    # histogram
    ccf_sequence = sorted([d for d in clustering_coefficient], reverse=True)
    ccf_count = collections.Counter(ccf_sequence)
    ccf, cnt = zip(*ccf_count.items())

    ccf_x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    cnt_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for key, value in dict(zip(ccf, cnt)).items():
        if key <= 0.05:
            cnt_y[0] += value
        elif key > 0.05 and key <= 0.15:
            cnt_y[1] += value
        elif key > 0.15 and key <= 0.25:
            cnt_y[2] += value
        elif key > 0.25 and key <= 0.35:
            cnt_y[3] += value
        elif key > 0.35 and key <= 0.45:
            cnt_y[4] += value
        elif key > 0.45 and key <= 0.55:
            cnt_y[5] += value
        elif key > 0.55 and key <= 0.65:
            cnt_y[6] += value
        elif key > 0.65 and key <= 0.75:
            cnt_y[7] += value
        elif key > 0.75 and key <= 0.85:
            cnt_y[8] += value
        elif key > 0.85 and key <= 0.95:
            cnt_y[9] += value
        elif key > 0.95:
            cnt_y[10] += value
    data = pd.DataFrame({
        'local clustering coefficient': ccf_x,
        'number of nodes': cnt_y
    })

    plt.clf()
    sns.set(style="whitegrid", font_scale=4)
    sns.set_style({'font.sans-serif': ['Times New Roman']})
    plt.figure(figsize=(12, 12))
    sns.barplot(x='local clustering coefficient', y='number of nodes', data=data, palette="Purples_d")

    plt.savefig('Current Network\\local_clustering_coefficient_distribution.png', format='PNG', bbox_inches='tight')


if __name__ == '__main__':
    G = nx.MultiGraph()

    # exist now
    operation = "select satoshis,nodes,(open :: json ->'time') from public.channels where ( close :: json -> 'time' ):: TEXT like 'null' "
    Graph_Construct(operation, G)

    node_capacity_distribution(G)
    channel_capacity_distribution(G)
    degree_distribution_fitting(G)
    G0 = nx.Graph(G)
    clustering_coefficient_distribution(G0)
 
    # closed channels--lifetime
    # operation = "select satoshis,nodes,(open :: json ->'time'),(close :: json ->>'time') from public.channels where ( close :: json -> 'time' ):: TEXT not like 'null' "
    # Graph_Construct_closedchannels(operation, G)
    # channel_capacity_distribution(G)
