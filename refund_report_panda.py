import os
import pandas as pd
from datetime import datetime

# Data directory
data_dir = "data"
output_dir = "output"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load CSV files
order_item_refunds = pd.read_csv(f"{data_dir}/order_item_refunds.csv")
order_items = pd.read_csv(f"{data_dir}/order_items.csv")
orders = pd.read_csv(f"{data_dir}/orders.csv")
products = pd.read_csv(f"{data_dir}/products.csv")
website_pageviews = pd.read_csv(f"{data_dir}/website_pageviews.csv")

# Merge refunds with order_items to get product_id
refunds_with_items = order_item_refunds.merge(
    order_items[['order_item_id', 'product_id']],
    on='order_item_id',
    how='left'
)

# Rename refund created_at for clarity
refunds_with_items.rename(columns={'created_at': 'refund_created_at'}, inplace=True)

# Merge with products to get product_name
refunds_with_products = refunds_with_items.merge(
    products[['product_id', 'product_name']],
    on='product_id',
    how='left'
)

# Merge with orders to get order_created_at and website_session_id
refunds_with_orders = refunds_with_products.merge(
    orders[['order_id', 'created_at', 'website_session_id']],
    on='order_id',
    how='left'
)
refunds_with_orders.rename(columns={'created_at': 'order_created_at'}, inplace=True)

# Get first pageview URL per session
pageviews_first = website_pageviews.groupby('website_session_id')['pageview_url'].first().reset_index()

# Merge with website_pageviews to get pageview_url
refunds_complete = refunds_with_orders.merge(
    pageviews_first,
    on='website_session_id',
    how='left'
)

# Create the refund_report with required transformations
refund_report = pd.DataFrame()
refund_report['refund_created_date'] = pd.to_datetime(refunds_complete['refund_created_at']).dt.date
refund_report['order_id'] = refunds_complete['order_id']
refund_report['refund_amount'] = refunds_complete['refund_amount_usd']
refund_report['product_id'] = refunds_complete['product_id']
refund_report['product_name'] = refunds_complete['product_name']
refund_report['order_created_date'] = pd.to_datetime(refunds_complete['order_created_at']).dt.date

# Calculate order_duration in minutes
refund_created = pd.to_datetime(refunds_complete['refund_created_at'])
order_created = pd.to_datetime(refunds_complete['order_created_at'])
refund_report['order_duration'] = ((refund_created - order_created).dt.total_seconds() / 60).astype('Int64')

refund_report['pageview_url'] = refunds_complete['pageview_url']

# Save to CSV
refund_report.to_csv(f"{output_dir}/refund_report.csv", index=False)

print("Refund report generated successfully!")
print(f"Output saved to {output_dir}/refund_report.csv")
print(f"\nReport shape: {refund_report.shape}")
print(f"\nFirst few rows:")
print(refund_report.head())
