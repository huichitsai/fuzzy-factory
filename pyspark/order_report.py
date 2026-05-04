
import boto3
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def read_s3_file(bucket_name, file_key):
    # Get AWS credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'minio')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'minioadmin')
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    s3_endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL', 'http://localhost:9000')
    
    # Create S3 client with credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
        endpoint_url=s3_endpoint_url
    )
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    return content

def create_spark_session():
    # Get AWS credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'minio')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'minioadmin')
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    s3_endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL', 'http://localhost:9000')
    
    # Create Spark session with S3 configuration
    spark = SparkSession.builder \
        .appName("OrderReport") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
        .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint_url) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.hadoop.fs.s3a.experimental.aws.s3.listobjects.v1", "false") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
        .config("spark.driver.maxResultSize", "0") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.4.1") \
        .getOrCreate()
    return spark

def read_s3_to_spark(spark,bucket_name, file_key):
    # Read the CSV file from S3 into a Spark DataFrame
    df = spark.read.csv(f"s3a://{bucket_name}/{file_key}", header=True, inferSchema=True)
    return df

def write_spark_df_to_s3(df, bucket_name, output_key):
    # Write the Spark DataFrame back to S3 as a CSV file
    df.coalesce(1).write.csv(f"s3a://{bucket_name}/{output_key}", header=True, mode='overwrite')

def show_latest_orders(df, n=5):
    # Assuming the DataFrame has a timestamp column named 'order_created_at'
    latest_orders = df.orderBy(F.col('order_created_at').desc()).limit(n)
    latest_orders.show()

def join_orders_with_sessions_and_pageviews(orders_df, sessions_df, pageview_df):
    # Rename orders columns to avoid ambiguity after join
    orders_df = orders_df.select("order_id", "created_at", "website_session_id") 
    pageview_df = pageview_df.select("website_pageview_id", "website_session_id", "pageview_url")
    joined_df = pageview_df.join(orders_df, on='website_session_id', how='inner')
    return joined_df

def show_top_pageviews_with_orders(joined_df, n=5):
    # Show the top N pages that have most orders created
    top_pageviews = joined_df.groupBy("pageview_url") \
                             .agg(F.count_distinct("order_id").alias("order_count"),
                                  F.count_distinct("website_pageview_id").alias("visit_count"),
                                  F.max("created_at").alias("latest_order_time")) \
                             .orderBy(F.col("order_count").desc()) \
                             .limit(n)
    top_pageviews.select("pageview_url", "order_count", "visit_count", "latest_order_time").show()
    return top_pageviews

def main():
    source_bucket_name = "data"
    orders_file_key = "orders.csv"
    sessions_file_key = "website_sessions.csv"
    pageviews_file_key = "website_pageviews.csv"

    # content = read_s3_file(bucket_name, file_key)
    # print(content)
    spark = create_spark_session()
    order_df = read_s3_to_spark(spark, source_bucket_name, orders_file_key)
    session_df = read_s3_to_spark(spark, source_bucket_name, sessions_file_key)
    pageview_df = read_s3_to_spark(spark, source_bucket_name, pageviews_file_key)
    joined_df = join_orders_with_sessions_and_pageviews(order_df, session_df, pageview_df)
    top_pageviews = show_top_pageviews_with_orders(joined_df)
    write_spark_df_to_s3(top_pageviews, "reporting", "top_pageviews.csv")


if __name__ == "__main__":
    main()