-- The results of running the events per account per month SQL
SELECT
	account_id,
	ROUND (COUNT(event_type) / 6::decimal, 2)::text AS events_per_account_per_month
FROM 
	livebook.event
WHERE 
	event_time >= '2019-12-01'
	AND event_time < '2020-06-01'
GROUP BY 1


-- One example of running the events per day SQL and visualizing the result