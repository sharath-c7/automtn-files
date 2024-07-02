import botocore.session

def remove_cross_region_replication(buckets):
    session = botocore.session.get_session()
    client = session.create_client('s3')

    for bucket_name in buckets:
        # Disable and delete replication configuration
        client.delete_bucket_replication(
            Bucket=bucket_name
        )

        print(f"Cross-region replication removed for bucket '{bucket_name}'.")

# Example usage:
buckets_to_remove_replication = ['source-bdcrr-bucket-us-east-2', 'destination-bdcrr-bucket-us-east-22']

remove_cross_region_replication(buckets_to_remove_replication)
