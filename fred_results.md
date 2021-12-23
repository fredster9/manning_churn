## Chapter 1.1
https://liveproject.manning.com/module/602_2_1/customer-behavior/1--load-the-event-data-into-postgresql-and-run-analytics/1-1-workflow%3a-load-the-event-data-into-postgresql-and-run-analytics?

### Questions
Results from notebook: manning_customer_behavior_chap_1.py

#### Customer behavior 2

1. What events are most common?

| Event                 | Count   |
|-----------------------|---------:|
| "ReadingOwnedBook"    | 1496520 |
| "FirstLivebookAccess" | 1316452 |
| "FirstManningAccess"  | 1314680 |
| "EBookDownloaded"     | 554712  |
| "ReadingFreePreview"  | 276394  |

2. What events are least common?

| Event                             | Count |
|-----------------------------------|-------:|
| "ProductLiveaudioUpsell"          | 1676  |
| "ProductSeeFreeLinkOpened"        | 326   |
| "SherlockHolmesClueFound"         | 20    |
| "UnknownOriginLivebookLinkOpened" | 6     |
| "CommentCreated"                  | 2     |

3. How many events are there for which customers average more than (for example) 0.05 events per month? (You should find that, for many events, the average number is less than 1 per customer per month.)
    I may be doing this wrong because the only events that have more than 0.05 events per customer per day are "FirstLivebookAccess" and 
    "FirstManningAccess" which are weird outliers because they have a lot of events but only one customer.

#### Customer behavior 3
1. Do events happen equally every day, or are there patterns?
    A bunch a weekly cadence (dip on weekends), inc: FirstManningAccess, FirstLivebookAccess, LivebookLogin, the Reading... metrics, etc.
2. Are there any gaps in the record of any events?
    Yes: ProductSeeFreeLinkOpened,.
3. Are there any events that only occur in part of the history?
    Yes: LivbookRegistration, LivebookAccountConfirmation, FirstManningAccess and a couple more.
4. Are there any extreme outliers or anomalies in the number of events?
    FreeContentCheckout spikes Apr 19 after a surge - my guess is a one month promo of some sort. Similarly, ProductLiveaudioUpsell and a few more.

### Deliverable
1. The results of running the events per account per month SQL

|   |                  event_type | n_events | n_customers | events_per_cust |  n_month | events_per_cust_per_mon |
|--:|----------------------------:|---------:|------------:|----------------:|---------:|------------------------:|
| 0 |           AddOrUpdateCoupon |     2554 |         730 |               3 | 6.678571 |                0.000573 |
| 1 |          AddProductOffering |    13022 |        4421 |               2 | 6.678571 |                0.000382 |
| 2 |             BookmarkCreated |    21800 |        1775 |              12 | 6.678571 |                0.002292 |
| 3 |              CommentCreated |        2 |           1 |               2 | 6.678571 |                0.000382 |
| 4 |    CrossReferenceTermOpened |    68188 |        7332 |               9 | 6.678571 |                0.001719 |
| 5 | DashboardLivebookLinkOpened |    96616 |       11283 |               8 | 6.678571 |                0.001528 |

    > this is wrong because it's events per accounts that had that event, not ALL events

2. One example of running the events per day SQL and visualizing the result

![Metric by day](/chap1_eventy_by_day.png)

