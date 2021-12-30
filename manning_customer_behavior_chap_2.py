
# %% [markdown]
### Workflow
# 1. [x] Create a table to hold the metrics in your schema by modifying and then running the listing create_metric.sql from the Fighting Churn with Data GitHub repository.
# 2. [x] Create the metric_type_name table using create_metric_name.sql from Fighting Churn with Data.
# 3. [] Calculate “basic” customer metrics for the more common events. A basic customer metric, in this context, is a count of the events a customer had in the recent past. You can use listing 3.3, count metric insert statement from Fighting Churn with Data as a starting point, but you need to modify it to fit the data from the project.
# 4. [] Calculate metric summary stats and include what percent of accounts have nonzero values on each metric. These will help you summarize the metrics you have created. You can use listing 3.8, metric coverage for this or write a similar SQL on your own. If you use listing 3.8, you still need to make some modifications to work with the liveBook schema.
# 5.Calculate metric statistics (average, minimum, and maximum) versus time and visualize them. You can use listing 3.6, metrics stats over time, and listing 3.7, metric qa plot. Or you can write a similar SQL and visualize the data using your own Python program or a spreadsheet (etc.).

# %%
## IMPORTS
import pandas as pd
import psycopg2
import plotly.express as px

# %%
## CONNECT TO DB
conn = psycopg2.connect(database="livebook", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")
print("Opened database successfully")

# %%
## TEST GETTING DATA 
query = '''
    SELECT
        event_type
        , COUNT(*)
    FROM 
        livebook.event
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 5
'''
df = pd.read_sql_query(query, con=conn)
df

# %%
top_events = ['ReadingOwnedBook', 'FirstLivebookAccess', 'FirstManningAccess', 
            'EBookDownloaded', 'ReadingFreePreview']

for event in top_events:
    metric_name = event+'_90d'
    with conn.cursor() as curs:
        curs.execute(
            """
            with date_vals AS (
                select i::timestamp as metric_date 
                from generate_series('2019-11-29', '2020-06-04', '7 day'::interval) i
            )
            -- insert into metric (account_id, metric_time, metric_name, metric_value)
            select 
                account_id, 
                metric_date AS metric_time,
                event_type AS metric_name,
                count(*) AS metric_value
            from livebook.event e inner join date_vals d
                on e.event_time < metric_date 
                and e.event_time >= metric_date - interval '90 day' -- does this inc. periods that are 90 days but not 90 days of data?
            where event_type=%s
            group by 1,2,3
            """, (event,))
        curs.fetchmany(10)
        # need to commit changes

# %%
## Viz avg event value over time - doing this for all metrics
query = '''
    with 
    date_range as (     
        select i::timestamp as calc_date 
    from generate_series('2019-12-01', '2020-06-04', '7 day'::interval) i -- why did i have to make it the 1st?
    ),

    the_metric as (  
        select * from livebook.metric m
        -- where metric_name_id = 0
    )

    select
        calc_date,  
        metric_name_id,
        avg(metric_value) AS avg_metric_value, 
        count(the_metric.*) as n_calc,
        min(metric_value), 
        max(metric_value)    
    from date_range left outer join the_metric on calc_date=metric_time     
    group by calc_date, metric_name_id    
    order by calc_date    
'''

df = pd.read_sql_query(query, con=conn)

fig = px.line(df, x="calc_date", y="avg_metric_value", color='metric_name_id')
fig.show()
