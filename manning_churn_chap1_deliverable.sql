-- I ended up downloading the partial and then full solutions.
-- I got fairly close on my own but not close enough.

---------

-- DROP TABLE livebook.observation;

---------

CREATE TABLE livebook.observation
(
    account_id character(32) COLLATE pg_catalog."default" NOT NULL,
    observation_date date NOT NULL,
    is_churn boolean
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE livebook.observation
    OWNER to postgres;

-- Index: idx_observation_account_date

CREATE UNIQUE INDEX idx_observation_account_date
    ON livebook.observation USING btree
    (account_id COLLATE pg_catalog."default", observation_date)
    TABLESPACE pg_default;

-- Index: observation_date_idx

CREATE INDEX observation_date_idx
    ON livebook.observation USING btree
    (observation_date)
    TABLESPACE pg_default;

---------

WITH first_use AS (
    SELECT
        account_id,
        product_id,
        MIN(event_time) AS first_use_time
    FROM livebook.event
    GROUP BY 1, 2
	ORDER BY 1,3
),

pre_0301_accounts AS (
    SELECT 
        DISTINCT account_id 
	FROM first_use
	WHERE first_use_time < CAST('2020-03-01' AS timestamp)
),

post_0301_accounts AS (
    SELECT 
        DISTINCT account_id 
	FROM first_use
	WHERE first_use_time >= CAST('2020-03-01' AS timestamp)
)

insert into livebook.observation (account_id, observation_date, is_churn)

SELECT
    DISTINCT pre.account_id,
	CAST('2020-03-01' as date) as observation_date,
	CASE WHEN post.account_id IS NULL THEN TRUE ELSE FALSE END AS is_churn
FROM pre_0301_accounts pre
LEFT JOIN
    post_0301_accounts post
    ON pre.account_id = post.account_id
	
---------

-- churn calcs

SELECT
	is_churn,
	COUNT(*),
	( COUNT (*) / SUM(COUNT(*)) OVER () ) * 100 AS rate
FROM 
	livebook.observation
GROUP BY 1

-- 67% retention rate