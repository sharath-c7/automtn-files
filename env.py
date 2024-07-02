import os

# Setting environment variables
os.environ['KEY'] = 'value'
os.environ['ANOTHER_KEY'] = 'another_value'

# Accessing environment variables
key_value = os.getenv('KEY')
print(key_value)  # Output: value
