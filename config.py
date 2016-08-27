SERVER_HOST = "200.129.38.153"

LOGIN = "root"
PASSWORD = "root7685"
COLLECTOR_ID = "b8599899-093f-4c59-a36b-4cb23476bf2d"

# Override with atual colector position
LATITUDE = -4.864177
LONGITUDE = -39.581899

# Define a location to local database
DATABASE_DIR = "/home/felipepinho/SistemaV4/RadarLivreCollector/data"
DATABASE_DIR = "/home/felipe/Projects/WEB/RadarLivre/RadarLivreCollector/data"

# Define a location to log files
LOG_DIR = "/home/felipepinho/SistemaV4/RadarLivreCollector/log"
LOG_DIR = "/home/felipe/Projects/WEB/RadarLivre/RadarLivreCollector/log"

# Override with the collector adress, normaly located in /dev/ttyACM...
COLLECTOR_ADDRESS = '/dev/ttyACM0'

# 10 seconds. After this time, the not sent messages will be deleteds
MAX_MESSAGE_AGE = 60 * 1000

DATA_OUTPUT_ENABLED = True
DATA_OUTPUT_HOST = "127.0.0.1"
DATA_OUTPUT_PORT = 30003

LOCAL_DATA_ENABLED = False
