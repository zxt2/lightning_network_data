import matplotlib.pyplot as plt
import json
import pandas as pd
import seaborn as sns
import networkx as nx
import powerlaw
import lnanalysis_monthly_data
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'

monthly = ['2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01', '2018-06-01', '2018-07-01', '2018-08-01',
           '2018-09-01', '2018-10-01', '2018-11-01', '2018-12-01',
           '2019-01-01', '2019-02-01', '2019-03-01', '2019-04-01', '2019-05-01', '2019-06-01', '2019-07-01',
           '2019-08-01', '2019-09-01', '2019-10-01', '2019-11-01', '2019-12-01',
           '2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01']
monthly_label = ['2018-02-01', ' ', '2018-04-01', '', '2018-06-01', '', '2018-08-01', '', '2018-10-01', '',
                 '2018-12-01',
                 '', '2019-02-01', '', '2019-04-01', '', '2019-06-01', '', '2019-08-01', '', '2019-10-01', '',
                 '2019-12-01',
                 '', '2020-02-01', '', '2020-04-01', '', '2020-06-01', '']

with open('monthly_data.json', 'r', encoding='UTF-8') as f:
    monthly_data = json.load(f)
	
    monthly_nodes = monthly_data['monthly_nodes']
    monthly_edges = monthly_data['monthly_edges']
    monthly_total_capacity = monthly_data['monthly_total_capacity']
    monthly_edges_average_capacity = monthly_data['monthly_edges_average_capacity']
    monthly_nodes_average_degree = monthly_data['monthly_nodes_average_degree']
    monthly_nodes_average_capacity = monthly_data['monthly_nodes_average_capacity']
    monthly_density = monthly_data['monthly_density']
    monthly_alpha = monthly_data['monthly_alpha']

line_width = 8
marker_size = 15
markeredge = 3
font_size = 40
rotating = 60
font_size1 = 25


def fitting_trend(time, monthly_a):
    # fitting trend
    monthly_a = [round(alpha, 2) for alpha in monthly_a]
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.plot(time, monthly_a, linestyle='-', linewidth=5, color='#3399FF')
    ax.set_ylim(2.0, 2.3)
    ax.set_xlabel('date', fontsize=font_size)
    ax.set_ylabel('alpah', fontsize=font_size)
    ax.set_xticklabels(monthly_label)
    for tick in ax.get_xticklabels():
        tick.set_rotation(rotating)
    ax.tick_params(labelsize=font_size)
    ax.grid(axis='y')

    ax.plot('2019-05-01', 2.21, marker='o', markersize=12, color='gray')
	plt.quiver('2019-05-01', 2.21, 1, 0, scale=7.8, width=0.0015, color='k',headwidth=5)

    # degree data preparing
    Gfit = nx.MultiGraph()
    operation = "select satoshis,nodes from public.channels where ( (( close->'time' ):: text like 'null') or ((close ->>'time')::text::integer > 1556640000) ) and ((open ->>'time')::text::integer <= 1556640000)"
    lnanalysis_get_monthly_data.Graph_Construct(operation, Gfit)
    degree = []
    for node in Gfit.nodes():
        degree.append(Gfit.degree(node))

    data = degree
    fit = powerlaw.Fit(data, discrete=True)

    numberlist = list(set(degree))
    dict = {}
    for item in numberlist:
        dict[item] = degree.count(item)
    # calculation proportion
    totalcount = sum(list(dict.values()))
    for k, v in dict.items():
        dict[k] = v / totalcount

    # degree fitting
    ax1 = inset_axes(ax, width="25%", height="35%", loc='upper center',bbox_to_anchor=(0.27,-0.08,1,1),bbox_transform=ax.transAxes)
    ax1.scatter(list(dict.keys()), list(dict.values()), marker='x', c='#3366CC', alpha=0.8, s=25)
    ax1.set_xlim(10 ** 0, 10 ** 4)
    ax1.set_ylim(10 ** -4, 10 ** 0)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    frame = plt.gca()
    frame.axes.get_yaxis().set_visible(False)
    frame.axes.get_xaxis().set_visible(False)
    
    fit.power_law.plot_pdf(linestyle='--', linewidth='2.5', c='k')
    ax1.text(10 ** 1.6, 10 ** -1.5, "$y\sim x^{%.2f}$" % (-fit.power_law.alpha), size=35)

    plt.savefig('Time Dimension\\degree_distribution_alpha.png', format='PNG', bbox_inches='tight')


def scale(time):
    BTC = []
    for i in monthly_total_capacity:
        BTC.append(i / 100000000)

    fig = plt.figure(figsize=(20, 13.5))
    host = fig.add_subplot(111)
    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    p1, = host.plot(time, monthly_nodes, linestyle='--', marker='o', markerfacecolor='white', markersize=marker_size,
                    markeredgewidth=markeredge, linewidth=line_width, color='#990033', label="nodes")
    p2, = par1.plot(time, monthly_edges, linestyle='-.', marker='s', markerfacecolor='white', markersize=marker_size,
                    markeredgewidth=markeredge, linewidth=line_width, color='#0066CC', label="channels")
    p3, = par2.plot(time, BTC, linestyle=':', marker='^', markerfacecolor='white', markersize=marker_size,
                    markeredgewidth=markeredge, linewidth=line_width, color='#660099', label="total capacity")
    p4, = par3.plot(time, monthly_density, linestyle='-', marker='D', markerfacecolor='white', markersize=marker_size,
                    markeredgewidth=markeredge, linewidth=line_width, color='#CC9900', label="density")
    lns = [p1, p2, p3, p4]
    host.legend(handles=lns, loc='upper left', fontsize=font_size)

    # right, left, top, bottom
    par2.spines['right'].set_position(('outward', 140))
    par3.spines['right'].set_position(('outward', 270))

    host.set_ylim(0, 8000)
    par1.set_ylim(0, 45000)
    par2.set_ylim(0, 1200)
    par3.set_ylim(0, 0.025)
    host.set_xlabel('date', fontsize=font_size)
    host.set_ylabel("nodes", fontsize=font_size)
    par1.set_ylabel("channels", fontsize=font_size)
    par2.set_ylabel("total capacity (BTC)", fontsize=font_size)
    par3.set_ylabel("density", fontsize=font_size)
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())

    host.set_xticklabels(monthly_label)
    host.tick_params(labelsize=font_size)
    par1.tick_params(labelsize=font_size)
    par2.tick_params(labelsize=font_size)
    par3.tick_params(labelsize=font_size)

    for tick in host.get_xticklabels():
        tick.set_rotation(rotating)
    plt.grid(axis='y')
    plt.savefig('Time Dimension\\scale.png', format='PNG', bbox_inches='tight')


def features(time):
    node_mBTC = []
    for i in monthly_nodes_average_capacity:
        node_mBTC.append(i / 100000)
    channel_mBTC = []
    for i in monthly_edges_average_capacity:
        channel_mBTC.append(i / 100000)

    fig = plt.figure(figsize=(18, 12))
    host = fig.add_subplot(111)
    par1 = host.twinx()
    par2 = host.twinx()

    p1, = host.plot(time, monthly_nodes_average_degree, linestyle='-', marker='o', markerfacecolor='white',
                    markersize=marker_size, markeredgewidth=markeredge, linewidth=line_width, color='#990033',
                    label="average degree")
    p2, = par1.plot(time, node_mBTC, linestyle='-', marker='s', markerfacecolor='white', markersize=marker_size,
                    markeredgewidth=markeredge,
                    linewidth=line_width, color='#0066CC', label="average capacity of nodes")
    p3, = par2.plot(time, channel_mBTC, linestyle='-', marker='^', markerfacecolor='white', markersize=marker_size,
                    markeredgewidth=markeredge,
                    linewidth=line_width, color='#CC9900', label="average capacity of channels")
    lns = [p1, p2, p3]
    host.legend(handles=lns, loc='lower right', fontsize=font_size)

    # right, left, top, bottom
    par2.spines['right'].set_position(('outward', 130))

    host.set_ylim(0, 16)
    par1.set_ylim(0, 200)
    par2.set_ylim(0, 30)
    host.set_xlabel('date', fontsize=font_size)
    host.set_ylabel("average degree", fontsize=font_size)
    par1.set_ylabel("average capacity of nodes (${10^{-3}}$BTC)", fontsize=font_size)
    par2.set_ylabel("average capacity of channels (${10^{-3}}$BTC)", fontsize=font_size)
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    host.set_xticklabels(monthly_label)
    host.tick_params(labelsize=font_size)
    par1.tick_params(labelsize=font_size)
    par2.tick_params(labelsize=font_size)

    for tick in host.get_xticklabels():
        tick.set_rotation(rotating)
    plt.grid(axis='y')
    plt.savefig('Time Dimension\\features.png', format='PNG', bbox_inches='tight')


if __name__ == '__main__':
    
	fitting_trend(monthly, monthly_alpha)
    scale(monthly)
    features(monthly)
	
    # correlation coefficient between pairs
    data = pd.DataFrame({
        'node': monthly_nodes,
        'channel': monthly_edges,
        'total_cap': monthly_total_capacity,
        'node_avg_deg': monthly_nodes_average_degree,
        'node_avg_cap': monthly_nodes_average_capacity,
        'channel_avg_cap': monthly_edges_average_capacity
    })
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # print(data.corr())
    # print(data.corr('spearman'))
    
    sns.set(font_scale=2.75)
    sns.set_style({'font.sans-serif': ['Times New Roman']})
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(data.corr(), annot=True,cmap='Purples')
    plt.title('Pearson',fontsize=35)
    plt.tight_layout()
    plt.savefig('Time Dimension\\Pearson.png', format='PNG')
    
    plt.clf()   
    plt.figure(figsize=(12, 10))
    sns.heatmap(data.corr('spearman'), annot=True,cmap='Greens')
    plt.title('Spearman',fontsize=35)
    plt.tight_layout()
    plt.savefig('Time Dimension\\Spearman.png', format='PNG')

    
