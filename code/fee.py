import psycopg2
import networkx as nx
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Times New Roman'
rcParams['mathtext.fontset'] = 'stix'

conn = psycopg2.connect(database="lndata", user="postgres",
                        password="postgres", host="127.0.0.1", port="5432")
cursor = conn.cursor()
cursor.execute("SELECT * FROM public.network")
rows = cursor.fetchall()
cursor.close()
conn.close()

font_size1=40
font_size2 = 35

G = nx.MultiDiGraph()
for row in rows:
    if row[4] == 0:
        G.add_edge(row[3], row[2], balance=row[1], basis=row[5], slope=row[6])
    if row[4] == 1:
        G.add_edge(row[2], row[3], balance=row[1], basis=row[5], slope=row[6])

base = []
slope = []
balance = []
for u, v in G.edges():
    for i in range(len(G[u][v])):
        base.append(int(G[u][v][i]['basis']))
        slope.append(int(G[u][v][i]['slope']))
        balance.append(int(G[u][v][i]['balance']))

for i in range(len(base)):
    base[i]/=1000

# # base fee distribution
# i0 = 0
# i1 = 0
# i2 = 0
# for item in base:
#     if item < 1000:
#         i0 += 1
#     elif item == 1000:
#         i1 += 1
#     else:
#         i2 += 1
#
# data = [i0, i1, i2]
# labels = ['<1000', '=1000', '>1000']
# plt.pie(x=data, labels=labels, autopct='%.3f%%')
# plt.savefig('Transaction Fee\\base_fee_distribution.png', format='PNG', bbox_inches='tight')


# # fee rate distribution
# i0 = 0
# i1 = 0
# i2 = 0
# i3 = 0
# for item in slope:
#     if item <= 10:
#         i0 += 1
#     elif item <= 100:
#         i1 += 1
#     elif item <= 1000:
#         i2 += 1
#     else:
#         i3 += 1
#
# data = [i0, i1, i2, i3]
# labels = ['<=10', '10~100', '100~1000', '>1000']
# plt.clf()
# plt.pie(x=data, labels=labels, autopct='%.3f%%')
# plt.savefig('Transaction Fee\\fee_rate_distribution.png', format='PNG', bbox_inches='tight')


# base fee CDF
ecdf = sm.distributions.ECDF(base)
x = np.linspace(min(base), 2.5)
y = ecdf(x)

plt.figure(figsize=(10,10))
plt.step(x, y,linewidth=4, color='#660099')
plt.xlim(0, 2.5)
plt.ylim(0, 1.1)
plt.xlabel('base fee (sat)',fontsize=font_size1)
plt.ylabel('CDF',fontsize=font_size1)
plt.tick_params(labelsize=font_size1)
plt.grid()
plt.savefig('Transaction Fee\\base_fee_CDF.png', format='PNG', bbox_inches='tight')


# fee rate CDF
ecdf = sm.distributions.ECDF(slope)
x = np.linspace(min(base), 10)
# x = np.linspace(min(slope), max(slope))
y = ecdf(x)

plt.figure(figsize=(10,10))
plt.step(x, y,linewidth=4, color='#660099')
plt.xlim(0, 10)
plt.ylim(0, 1.1)
plt.xlabel('fee rate (${10^{-6}}$)',fontsize=font_size1)
plt.ylabel('CDF',fontsize=font_size1)
plt.tick_params(labelsize=font_size1)
plt.grid()
plt.savefig('Transaction Fee\\fee_rate_CDF.png', format='PNG', bbox_inches='tight')


# relationship between base fee and balance
baselist = list(set(base))
baselist.sort()
dict = {}
ba = []
for item in baselist:
    if item <= 2:
        indexlist = [k for k, x in enumerate(base) if x == item]
        for j in indexlist:
            ba.append(balance[j])
        dict[item] = sum(ba) / len(ba)
        ba = []

cBTC_balance = []
for bal in list(dict.values()):
    cBTC_balance.append(bal / 1000000)

plt.clf()
plt.figure(figsize=(12, 8))
plt.scatter(list(dict.keys()), cBTC_balance, marker='x', c='#660099', alpha=0.8, s=40)
plt.xlim(0, 2)
plt.ylim(0, 25)
plt.xlabel('base fee (sat)', fontsize=font_size2)
plt.ylabel('average channel capacity (${10^{-2}}$BTC)', fontsize=font_size2)
plt.tick_params(labelsize=font_size2)
plt.grid()
plt.savefig('Transaction Fee\\base_fee_balance.png', format='PNG', bbox_inches='tight')

# relationship between fee rate and balance
slopelist = list(set(slope))
slopelist.sort()
dict = {}
ba = []
for item in slopelist:
    if item <= 200:
        indexlist = [k for k, x in enumerate(slope) if x == item]
        for j in indexlist:
            ba.append(balance[j])
        dict[item] = sum(ba) / len(ba)
        ba = []

cBTC_balance = []
for bal in list(dict.values()):
    cBTC_balance.append(bal / 1000000)

plt.clf()
plt.figure(figsize=(12, 8))
plt.scatter(list(dict.keys()), cBTC_balance, marker='x', c='#6600FF', alpha=0.8, s=40)
plt.xlim(0, 200)
plt.ylim(0, 20)
plt.xlabel('fee rate (${10^{-6}}$)', fontsize=font_size)
plt.ylabel('average channel capacity (${10^{-2}}$BTC)', fontsize=font_size)
plt.tick_params(labelsize=font_size)
plt.grid()
plt.savefig('Transaction Fee\\fee_rate_balance1.png', format='PNG', bbox_inches='tight')

slopelist = list(set(slope))
slopelist.sort()
dict = {}
ba = []
for item in slopelist:
    if item <= 2000:
        indexlist = [k for k, x in enumerate(slope) if x == item]
        for j in indexlist:
            ba.append(balance[j])
        dict[item] = sum(ba) / len(ba)
        ba = []

cBTC_balance = []
for bal in list(dict.values()):
    cBTC_balance.append(bal / 1000000)

plt.clf()
plt.figure(figsize=(12, 8))
plt.scatter(list(dict.keys()), cBTC_balance, marker='x', c='#6600FF', alpha=0.8, s=40)
plt.xlim(0, 2000)
plt.ylim(0, 20)
plt.xlabel('fee rate (${10^{-6}}$)', fontsize=font_size)
plt.ylabel('average channel capacity (${10^{-2}}$BTC)', fontsize=font_size)
plt.tick_params(labelsize=font_size)
plt.grid()
plt.savefig('Transaction Fee\\fee_rate_balance2.png', format='PNG', bbox_inches='tight')
