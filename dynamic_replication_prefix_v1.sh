#!/bin/bash
set -euo pipefail

# Function to configure replication for each prefix
configure_replication() {
    local source_bucket="$1"
    local destination_bucket="$2"
    local role_arn="$3"
    local prefixes=("${@:4}")  # Get all arguments starting from the 4th (prefixes)

    # Construct the replication rules array
    local rules=""
    for prefix in "${prefixes[@]}"; do
        rules+="{
            \"Status\": \"Enabled\",
            \"Destination\": {
                \"Bucket\": \"arn:aws:s3:::$destination_bucket\"
            },
            \"Prefix\": \"$prefix\"
        },"
    done

    # Remove the trailing comma from the last rule
    rules="${rules%,}"

    # Configure replication and log output
    if ! aws s3api put-bucket-replication --bucket "$source_bucket" --replication-configuration '{
        "Role": "'"$role_arn"'",
        "Rules": [
            '"$rules"'
        ]
    }' > replication.log 2>&1; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Replication configuration failed" >> replication.log
        exit 1
    fi

    # Log success
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Replication configuration successful" >> replication.log
}

# Example usage:
source_bucket="src-replication-bucket-us-east-1-c721"
destination_bucket="destn-replication-bucket-us-east-2-c721"
role_arn="arn:aws:iam::907537795685:role/s3crr-role-src-replication-bucket-us-east-1"

# Example prefixes (modify or add as needed)
prefixes=(
    "AdminFolder/Bre1/bred"
    "AdminFolder/Bre2/nerd"
    "Database/Bre1/bred"
    "Database/Bre2/nerd"
)

# Trap any errors and log them
trap 'echo "Error occurred in script at line $LINENO: $BASH_COMMAND"; exit 1' ERR

# Call function to configure replication
configure_replication "$source_bucket" "$destination_bucket" "$role_arn" "${prefixes[@]}"
