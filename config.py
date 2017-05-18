# Defines where the server is located
SERVER_HOST = "127.0.0.1:8000"

#Change this to match the superuser you created
LOGIN = "username"
PASSWORD = "password123"

#Change this to match the collector you created
COLLECTOR_ID = "29384c61-c588-488f-9390-52251d6491ed"

# Define a path to local database
DATABASE_DIR = "data"

# Define a path to log files
LOG_DIR = "log"

# Override with the collector adress, normaly located in /dev/ttyACM...
COLLECTOR_ADDRESS = '/dev/ttyACM0'

# 60 seconds. After this time, the not sent messages will be deleteds. Meassured in milliseconds
MAX_MESSAGE_AGE = 60 * 1000

DATA_OUTPUT_ENABLED = False
DATA_OUTPUT_HOST = "127.0.0.1"
DATA_OUTPUT_PORT = 30003

LOCAL_DATA_ENABLED = False
