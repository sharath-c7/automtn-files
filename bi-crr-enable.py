import botocore.session

def enable_bidirectional_replication(source_bucket, destination_bucket, source_region, destination_region):
    session = botocore.session.get_session()
    client = session.create_client('s3')

    # Configure replication rules for both directions
    replication_config_source = {
        'Role': 'arn:aws:iam::907537795685:role/service-role/s3crr_role_for_mycrrbucket1234',  # Replace with your IAM role ARN
        'Rules': [
            {
                'ID': f'AdminDatabaseReplicateToDestination',
                'Status': 'Enabled',
                'Prefix': 'AdminDatabase',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{destination_bucket}',
                    'StorageClass': 'STANDARD'
                }
            },
            {
                'ID': f'DatabaseReplicateToDestination',
                'Status': 'Enabled',
                'Prefix': 'Database',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{destination_bucket}',
                    'StorageClass': 'STANDARD'
                }
            }            
        ]
    }

    replication_config_destination = {
        'Role': 'arn:aws:iam::907537795685:role/service-role/s3crr_role_for_mycrrbucket1234',  # Replace with your IAM role ARN
        'Rules': [
            {
                'ID': f'AdminDatabaseReplicateToSource',
                'Status': 'Enabled',
                'Prefix': 'AdminDatabase',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{source_bucket}',
                    'StorageClass': 'STANDARD'
                }
            },
            {
                'ID': f'DatabaseReplicateToSource',
                'Status': 'Enabled',
                'Prefix': 'Database',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{source_bucket}',
                    'StorageClass': 'STANDARD'
                }
            }            
        ]
    }

    # Enable replication for source bucket
    client.put_bucket_replication(
        Bucket=source_bucket,
        ReplicationConfiguration=replication_config_source
    )

    # Enable replication for destination bucket
    client.put_bucket_replication(
        Bucket=destination_bucket,
        ReplicationConfiguration=replication_config_destination
    )

    print(f"Bidirectional replication enabled between '{source_bucket}' in region '{source_region}' and '{destination_bucket}' in region '{destination_region}'.")

# Example usage:
source_bucket_name = 'source-bdcrr-bucket-us-east-2'
destination_bucket_name = 'destination-bdcrr-bucket-us-east-22'
source_region_name = 'us-east-1'  # Replace with the source bucket's region
destination_region_name = 'us-east-2'  # Replace with the destination bucket's region

enable_bidirectional_replication(source_bucket_name, destination_bucket_name, source_region_name, destination_region_name)
