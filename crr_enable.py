import botocore.session

def enable_cross_region_replication(source_bucket, destination_bucket, destination_region):
    session = botocore.session.get_session()
    client = session.create_client('s3')

    # Configure replication rules
    replication_config = {
        'Role': 'arn:aws:iam::907537795685:role/service-role/s3crr_role_for_mycrrbucket1234',  # Replace with your IAM role ARN
        'Rules': [
            {
                'ID': 'AdminDatabaseRule1',
                'Status': 'Enabled',
                'Prefix': 'AdminDatabase',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{destination_bucket}',
                    'StorageClass': 'STANDARD'
                }
            },
            {
                'ID': 'DatabaseRule1',
                'Status': 'Enabled',
                'Prefix': 'Database',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{destination_bucket}',
                    'StorageClass': 'STANDARD'
                }
            },            
        ]
    }

    # Enable replication for the bucket
    client.put_bucket_replication(
        Bucket=source_bucket,
        ReplicationConfiguration=replication_config
    )

    print(f"Cross-region replication enabled for bucket '{source_bucket}' to '{destination_bucket}' in region '{destination_region}'.")

# Example usage:
source_bucket_name = 'source-bdcrr-bucket-us-east-2'
destination_bucket_name = 'destination-bdcrr-bucket-us-east-22'
destination_region_name = 'us-east-2'  # Replace with the destination region

enable_cross_region_replication(source_bucket_name, destination_bucket_name, destination_region_name)
