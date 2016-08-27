from receptor import rootConfig

rootConfig.SERVER_HOST = "200.129.38.153"

rootConfig.LOGIN = "root"
rootConfig.PASSWORD = "root7685"
rootConfig.COLLECTOR_ID = "b8599899-093f-4c59-a36b-4cb23476bf2d"

# Define a location to local database
rootConfig.DATABASE_DIR = "/home/felipepinho/SistemaV4/RadarLivreCollector/data"
rootConfig.DATABASE_DIR = "/home/felipe/Projects/WEB/RadarLivre/RadarLivreCollector/data"

# Define a location to log files
rootConfig.LOG_DIR = "/home/felipepinho/SistemaV4/RadarLivreCollector/log"
rootConfig.LOG_DIR = "/home/felipe/Projects/WEB/RadarLivre/RadarLivreCollector/log"

# Override with the collector adress, normaly located in /dev/ttyACM...
rootConfig.COLLECTOR_ADDRESS = '/dev/ttyACM0'

# 10 seconds. After this time, the not sent messages will be deleteds
rootConfig.MAX_MESSAGE_AGE = 60 * 1000

rootConfig.DATA_OUTPUT_ENABLED = True
rootConfig.DATA_OUTPUT_HOST = "127.0.0.1"
rootConfig.DATA_OUTPUT_PORT = 30003

rootConfig.LOCAL_DATA_ENABLED = False
