import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import statsmodels.api as sm

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Times New Roman'
rcParams['font.size'] = 30

conn = psycopg2.connect(database="lndata", user="postgres",
                        password="postgres", host="127.0.0.1", port="5432")
cursor = conn.cursor()
cursor.execute("SELECT * FROM public.channels")
rows = cursor.fetchall()
cursor.close()
conn.close()

font_size = 40

# # channel closing type
# closetype = []
# for row in rows:
#     close = row[4]
#     if close['fee'] != None:
#         closetype.append(close['type'])
#
# print(list(set(closetype)))
# dict = {}
# for item in list(set(closetype)):
#     dict[item] = closetype.count(item)
# print(dict)
# data = list(dict.values())
# labels = list(dict.keys())
#
# plt.clf()
# plt.figure(figsize=(8, 8))
# explode = [0, 0.2, 0, 0.1]
# plt.pie(x=data, labels=labels,autopct='%.3f%%', explode=explode)
# plt.savefig('Time Dimension\\channel_closing_types.png', format='PNG', bbox_inches='tight')

openchannel=[]
closechannel=[]
for row in rows:
    close = row[4]
    open = row[5]
    if close['fee'] == None:
        timec = 1595360049 - open['time']
        openchannel.append(timec)
    else:
        timec = int(close['time']) - open['time']
        closechannel.append(timec)

openchannel_day = []
for i in openchannel:
    i/=86400
    openchannel_day.append(i)

closechannel_day = []
for i in closechannel:
    i/=86400
    closechannel_day.append(i)

# closed channel lifetime
ecdf = sm.distributions.ECDF(closechannel_day)
x = np.linspace(min(closechannel_day), max(closechannel_day))
y = ecdf(x)

plt.figure(figsize=(10,10))
plt.step(x, y,linewidth=4, color='#3399FF')
plt.xlim(0, 1000)
plt.ylim(0, 1.1)
plt.xlabel('channel lifetime (day)',fontsize=font_size)
plt.ylabel('CDF',fontsize=font_size)
plt.tick_params(labelsize=font_size)
plt.grid()
plt.savefig('Time Dimension\\closed_channel_lifetime.png', format='PNG', bbox_inches='tight')

# closed channel lifetime
ecdf = sm.distributions.ECDF(openchannel_day)
x = np.linspace(min(openchannel_day), max(openchannel_day))
y = ecdf(x)

plt.figure(figsize=(10,10))
plt.step(x, y,linewidth=4, color='#3399FF')
plt.xlim(0, 1000)
plt.ylim(0, 1.1)
plt.xlabel('channel lifetime (day)',fontsize=font_size)
plt.ylabel('CDF',fontsize=font_size)
plt.tick_params(labelsize=font_size)
plt.grid()
plt.savefig('Time Dimension\\unclosed_channel_lifetime.png', format='PNG', bbox_inches='tight')
