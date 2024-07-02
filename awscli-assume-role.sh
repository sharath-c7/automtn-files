#!/bin/bash

# Function to assume IAM role with retry logic
assume_role_with_retry() {
    local role_arn="$1"
    local role_session_name="$2"
    local max_retries=3
    local retry_interval=5  # seconds
    local retry_attempt=0

    while [ $retry_attempt -lt $max_retries ]; do
        echo "Attempting to assume role: $role_arn (Attempt $((retry_attempt + 1)))..."

        # Attempt to assume role and capture credentials
        credentials=$(aws sts assume-role \
            --role-arn "$role_arn" \
            --role-session-name "$role_session_name" \
            --duration-seconds 3600 2>/dev/null)  # Redirect stderr to null to suppress error output

        # Check if assume-role command was successful
        if [ $? -eq 0 ] && [ -n "$credentials" ]; then
            # Extract and set AWS credentials from JSON response
            export AWS_ACCESS_KEY_ID=$(echo "$credentials" | jq -r '.Credentials.AccessKeyId')
            export AWS_SECRET_ACCESS_KEY=$(echo "$credentials" | jq -r '.Credentials.SecretAccessKey')
            export AWS_SESSION_TOKEN=$(echo "$credentials" | jq -r '.Credentials.SessionToken')
            echo "Successfully assumed role: $role_arn"
            return 0  # Success
        else
            echo "Failed to assume role: $role_arn (Attempt $((retry_attempt + 1)))"
            retry_attempt=$((retry_attempt + 1))
            sleep $retry_interval
        fi
    done

    echo "Failed to assume role after $max_retries attempts. Exiting."
    return 1  # Failure
}

# Example usage:
source_bucket="source-bucket-name"
destination_bucket="destination-bucket-name"
role_arn="arn:aws:iam::123456789012:role/xaccounts3access"
role_session_name="s3-access-example"

# Call function to assume role with retry logic
assume_role_with_retry "$role_arn" "$role_session_name"

# Check if assume role was successful before proceeding with AWS CLI operations
if [ $? -eq 0 ]; then
    # Example command: List S3 buckets using assumed role credentials
    aws s3 ls
else
    echo "Unable to assume role. Exiting."
fi

# Unset temporary credentials after use (optional)
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
