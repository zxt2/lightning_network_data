import psycopg2

## build a new table: network, including columns: short_channel_id,satoshis,node0,node1,direction,base_fee_millisatoshi,fee_per_millionth

## connect database
conn = psycopg2.connect(database="lndata", user="postgres",
                        password="postgres", host="127.0.0.1", port="5432")
## open cursor
cursor = conn.cursor()
cursor1 = conn.cursor()
cursor2 = conn.cursor()
## execute SQL SELECT
# cursor.execute("SELECT c.short_channel_id, c.satoshis, c.nodes, p.base_fee_millisatoshi, p.fee_per_millionth FROM public.channels c, public.policies p where ( c.close :: json -> 'fee' ):: TEXT like 'null' and c.short_channel_id = p.short_channel_id and p.direction = 1")
cursor.execute(
    "select short_channel_id, satoshis, nodes from public.channels where ( close :: json -> 'fee' ):: TEXT like 'null' ")
# cursor.execute("select * from public.policies where short_channel_id = '630905x2324x0' and direction = 1 order by update_time desc limit 1")

## get SELECT tuples
channels = cursor.fetchall()
for channel in channels:
    cursor1.execute(
        "select short_channel_id, base_fee_millisatoshi, fee_per_millionth from public.policies where short_channel_id = '" +
        channel[0] + "' and direction = 1 order by update_time desc limit 1")
    policy = cursor1.fetchall()

    if policy != []:
        print(channel[2][0], channel[2][1], policy[0][1], policy[0][2])
        cursor.execute(
            "insert into public.network(short_channel_id,satoshis,node0,node1,direction,base_fee_millisatoshi,fee_per_millionth) values('" +
            channel[0] + "'," + str(channel[1]) + ",'" + str(channel[2][0]) + "','" + str(channel[2][1]) + "',1," + str(
                policy[0][1]) + "," + str(policy[0][2]) + ")")
    else:
        cursor.execute(
            "insert into public.network(short_channel_id,satoshis,node0,node1,direction,base_fee_millisatoshi,fee_per_millionth) values('" +
            channel[0] + "'," + str(channel[1]) + ",'" + str(channel[2][0]) + "','" + str(channel[2][1]) + "',1,0,0)")

    cursor2.execute(
        "select short_channel_id, base_fee_millisatoshi, fee_per_millionth from public.policies where short_channel_id = '" +
        channel[0] + "' and direction = 0 order by update_time desc limit 1")
    policy1 = cursor2.fetchall()

    if policy1 != []:
        print(channel[2][0], channel[2][1], policy1[0][1], policy1[0][2])
        cursor.execute(
            "insert into public.network(short_channel_id,satoshis,node0,node1,direction,base_fee_millisatoshi,fee_per_millionth) values('" +
            channel[0] + "'," + str(channel[1]) + ",'" + str(channel[2][0]) + "','" + str(channel[2][1]) + "',0," + str(
                policy1[0][1]) + "," + str(policy1[0][2]) + ")")
    else:
        cursor.execute(
            "insert into public.network(short_channel_id,satoshis,node0,node1,direction,base_fee_millisatoshi,fee_per_millionth) values('" +
            channel[0] + "'," + str(channel[1]) + ",'" + str(channel[2][0]) + "','" + str(channel[2][1]) + "',0,0,0)")
## close cursor
cursor.close()
cursor1.close()
cursor2.close()
## close database connection
conn.commit()
conn.close()