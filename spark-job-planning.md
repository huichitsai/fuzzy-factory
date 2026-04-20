# Spark Job
Build reports using Spark
 
## sample refund reporting
### validate the idea
- create a python script: refund_report_panda.py
- use panda to generate a refund_report.csv with the columns below and save it under output directory

| Field | Data Source | Notes |
|-------|-------------|-------|
| refund_created_date | order_item_refunds.created_at | Date only (e.g., 2012-03-19) |
| order_id | order_item_refunds.order_id | |
| refund_amount | order_item_refunds.refund_amount_usd | |
| product_id | products.product_id | |
| product_name | products.product_name | |
| order_created_date | orders.created_at | Date only (e.g., 2012-03-19) |
| pageview_url | website_pageviews.pageview_url | |
| order_duration | order_item_refunds.created_at - orders.created_at | In minutes |

## create pyspark runtime environment in docker
### build custom pyspark image to include necessary libraries
```bash
# Build custom Spark image
docker build -t spark-custom:3.5.1 .
```
### build multi-cluster pyspark
[container/docker-compose.yml](container/docker-compose.yml)

### create a pyspark script
create a jupiter notebook python script as the function in refund_report_panda.py