# %%
## IMPORTS
import pandas as pd
import numpy as np
from configparser import ConfigParser
import psycopg2
import plotly.express as px


# %%
## CONNECT TO DB
conn = psycopg2.connect(database="livebook", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")

print("Opened database successfully")

cur = conn.cursor()

cur.execute("SELECT * FROM livebook.event LIMIT 10")
records = cur.fetchall()
records

# %%
## EVENTS COUNT
query = '''
    SELECT
        event_type
        , COUNT(*)
    FROM 
        livebook.event
    GROUP BY 1
    ORDER BY 2 DESC
'''
df = pd.read_sql_query(query, con=conn)
df

# %%
## ALL EVENTS PER CUSTOMER PER MONTH 
# this is not their solution bc i'm calculating customers by month vs all time
query = '''
    SELECT
        TO_CHAR(event_time, 'YYYY-MM')
        , COUNT(DISTINCT DATE_PART('day', event_time)) AS days_per_mon
        , COUNT(event_type) AS num_events
        , COUNT(DISTINCT account_id) AS num_customers
        , COUNT(event_type) / COUNT(DISTINCT account_id) AS events_per_cust_per_mon
        , COUNT(event_type) / COUNT(DISTINCT account_id) / COUNT(DISTINCT DATE_PART('day', event_time))::float AS events_per_cust_per_mon_per_day
    FROM 
        livebook.event
    GROUP BY 1
'''
df = pd.read_sql_query(query, con=conn)
df

# %%
## ALL EVENTS PER CUSTOMER PER MONTH 
# this is the book way of doing it - calcs all time accounts vs by mon
query = '''
    with 
    date_range as (    
    select  '2019-11-29'::timestamp as start_date,
        '2020-06-04'::timestamp as end_date
    ), account_count as (    
    select count(distinct account_id) as n_account
    from livebook.event
    )
    select e.event_type,
        count(*) as n_event,
        n_account as n_account,
        count(*)::float/n_account::float as events_per_account,
        extract(days from end_date-start_date)::float/28 as n_months,
        (count(*)::float/n_account::float)/(extract(days from end_date-start_date)::float/28.0)
            as events_per_account_per_month
    from livebook.event e cross join account_count
    inner join date_range ON
    event_time >= start_date
    and event_time <= end_date
    group by e.event_type,n_account,end_date,start_date
    order by events_per_account_per_month desc; 
'''
df = pd.read_sql_query(query, con=conn)
df
 

# %%
## INDIVIDUAL EVENTS PER CUSTOMER PER MONTH
query = '''
    SELECT
        event_type
        , COUNT(event_type) AS n_events
        , COUNT(DISTINCT account_id) AS n_customers 
        , COUNT(event_type) / COUNT(DISTINCT account_id)  AS events_per_cust
        ,  ( SELECT EXTRACT(days FROM (MAX(event_time) - MIN(event_time))) FROM livebook.event )::float/28.0 AS n_month -- doing this as regular row gets diff results for each event
        , COUNT(event_type) / COUNT(DISTINCT account_id) / ( SELECT EXTRACT(days FROM (MAX(event_time) - MIN(event_time))) FROM livebook.event )::float/28.0 AS events_per_cust_per_mon
    FROM 
        livebook.event
    GROUP BY 1
'''
df = pd.read_sql_query(query, con=conn)
df

# %%
## EVENT BEHAVIOR BY DAY
query = '''
    WITH 
        date_vals AS (    
            SELECT i::date AS metric_date
            FROM generate_series('2019-11-29', '2020-06-04',
            '1 day'::interval) i
    )

    SELECT
        metric_date
        , event_type
        , COUNT(event_type)
    FROM 
        livebook.event e
    LEFT OUTER JOIN date_vals d ON    
        DATE(event_time) = metric_date
    GROUP BY 1,2
'''
df = pd.read_sql_query(query, con=conn)
print(df)

fig = px.line(df, x="metric_date", y="count", color='event_type')
fig.show()

# %%
event_list = df['event_type'].unique()
for event in event_list:
    x = df[df['event_type']==event]
    print(event)
    fig = px.line(x, x="metric_date", y="count", range_x=['2019-11-29','2020-06-04'])
    fig.show()

range_x=['2016-07-01','2016-12-31']



# %%
## CONNECT DB -- this works but the other version is simpler, albeit less robust
# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()

#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
		
#         # create a cursor
#         cur = conn.cursor()
        
# 	# execute a statement
#         # print('PostgreSQL database version:')
#         # cur.execute('SELECT version()')
#         cur.execute('SELECT * FROM livebook.event LIMIT 10')

#         # display the PostgreSQL database server version
#         result = cur.fetchall()
#         print(result)
       
# 	# close the communication with the PostgreSQL
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')

# connect()
# %%
