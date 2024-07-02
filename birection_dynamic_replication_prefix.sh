#!/bin/bash
set -x
# Function to configure replication for each direction
configure_replication() {
    local source_bucket="$1"
    local destination_bucket="$2"
    local role_arn="$3"
    local prefixes=("${@:5}")  # Get all arguments starting from the 4th (prefixes)

    # Construct the replication rules array for source to destination
    local rules_source_to_dest=""
    for prefix in "${prefixes[@]}"; do
        rules_source_to_dest+="{
            \"Status\": \"Enabled\",
            \"Destination\": {
                \"Bucket\": \"arn:aws:s3:::$destination_bucket\"
            },
            \"Prefix\": \"$prefix\"
        },"
    done

    # Remove the trailing comma from the last rule
    rules_source_to_dest="${rules_source_to_dest%,}"

    # Configure replication from source to destination and log output
    aws s3api put-bucket-replication --bucket "$source_bucket" --replication-configuration '{
        "Role": "'"$src_role_arn"'",
        "Rules": [
            '"$rules_source_to_dest"'
        ]
    }' > replication_source_to_dest.log 2>&1

    # Construct the replication rules array for destination to source
    local rules_dest_to_source=""
    for prefix in "${prefixes[@]}"; do
        rules_dest_to_source+="{
            \"Status\": \"Enabled\",
            \"Destination\": {
                \"Bucket\": \"arn:aws:s3:::$source_bucket\"
            },
            \"Prefix\": \"$prefix\"
        },"
    done

    # Remove the trailing comma from the last rule
    rules_dest_to_source="${rules_dest_to_source%,}"

    # Configure replication from destination to source and log output
    aws s3api put-bucket-replication --bucket "$destination_bucket" --replication-configuration '{
        "Role": "'"$dst_role_arn"'",
        "Rules": [
            '"$rules_dest_to_source"'
        ]
    }' > replication_dest_to_source.log 2>&1

    # Check command exit status and log success or failure for both directions
    if [ $? -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Replication configuration from $source_bucket to $destination_bucket successful" >> replication.log
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Replication configuration from $destination_bucket to $source_bucket successful" >> replication.log
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Replication configuration from $source_bucket to $destination_bucket failed" >> replication.log
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Replication configuration from $destination_bucket to $source_bucket failed" >> replication.log
    fi
}

# Example usage:
source_bucket="src-replication-bucket-us-east-1-c721"
destination_bucket="destn-replication-bucket-us-east-2-c721"
src_role_arn="arn:aws:iam::907537795685:role/s3crr-role-src-replication-bucket-us-east-1"
dst_role_arn="arn:aws:iam::907537795685:role/s3crr-role-destn-replication-bucket-us-east-2"

# Example prefixes (modify or add as needed)
prefixes=(
    "AdminFolder/Bre1/bred"
    "AdminFolder/Bre2/nerd"
    "Database/Bre1/bred"
    "Database/Bre2/nerd"
)

# Call function to configure bidirectional replication
configure_replication "$source_bucket" "$destination_bucket" "$src_role_arn" "$dst_role_arn" "${prefixes[@]}"
