#/bin/bash
# The command above states wich shell is used

# This file is used to set up the project installing all requirements and dependencies
# Keep it as automated as possible, as the software must be easy enough for everyone to install
# Use ----- <Description> ----- to help users track installation proccess and possible errors.

# Every step is divided in sections as the following, so it is easier to track error and program

# Enter relative directory
BASEDIR=$(dirname "$0")
cd "$BASEDIR"
generateFile () {
	# The parameters can be acessed by using the variables $1, $2, $3 and $4
	# echo $1
	# echo $2
	# echo $3
	# echo $4

	# The following steps are going to create/replace the config file.
	# This is the file where we are going to store the configuration data.
	filename="config.py"

	# This is the command we use to clear the file, so, no need to check whether the file has been created or not.
	# echo "testfile">"$filename"
	# The following is slightly different. You keep the file intact while adding content to it.
	# echo "testfile">"$filename"

	# Comments about the config.py file.
	echo '# Read CONFIGURE.sh for details about this file.'>"$filename"
	echo '# You can still change this file directly, though it is not advised,'>>"$filename"
	echo '# if you do not know what you are doing.'>>"$filename"
	echo '# Read README.md for details.'>>"$filename"
	
	# Defines where the server is located
	echo "SERVER_HOST = \"$4\"">>"$filename"
	
	#Change this to match the superuser you created
	echo "LOGIN = \"$1\"">>"$filename"
	echo "PASSWORD = \"$2\"">>"$filename"

	#Change this to match the collector you created
	echo "COLLECTOR_ID = \"$3\"">>"$filename"

	# Define a path to local database
	echo "DATABASE_DIR = \"data\"">>"$filename"

	# Define a path to log files
	echo "LOG_DIR = \"log\"">>"$filename"

	# Override with the collector adress, normaly located in /dev/ttyACM...
	echo "COLLECTOR_ADDRESS = '/dev/ttyACM0'">>"$filename"

	# 60 seconds. After this time, the not sent messages will be deleteds. Meassured in milliseconds
	echo "MAX_MESSAGE_AGE = 60 * 1000">>"$filename"

	echo "DATA_OUTPUT_ENABLED = False">>"$filename"
	echo "DATA_OUTPUT_HOST = \"127.0.0.1\"">>"$filename"
	echo "DATA_OUTPUT_PORT = 30003">>"$filename"

	echo "LOCAL_DATA_ENABLED = False">>"$filename"
}

echo "************************************************************"
echo "| We are going to help you configure your collector now.   |"
echo "************************************************************"

echo '1. Please, provide your username:'
read username
#username="username"

echo '2. Please, provide your password:'
read password
#password="password"

echo "3. Please, enter your collector's ID(format: 12345678-1234-1234-1234-123456789012)"
echo 'You can copy it by typing CTRL+C and paste it in the terminal by typing SHIFT+CTRL+V'
echo 'Make sure to keep the "-"'
read collectorID
#collectorID="12345678-1234-1234-1234-123456789012"

echo '4. Please, enter where your server is located with the format "path\to\your\server:port".'
echo '127.0.0.1:8000 if running a local server.'
read serverHost
#serverHost="127.0.0.1:8000"

echo "Your username is $username."
echo "Your password is $password."
echo "Your collector's ID is $collectorID."
echo "Your server is located at $serverHost."

read -p "6. Confirm?(y/n)" -n 1 -r

# blank echo, so it does a line break
echo ''
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo '7. Generating your configuration file.'
    generateFile $username $password $collectorID $serverHost
    echo 'Done.'
    echo 'If you ever wish to reconfigure your collector, please, run this file again.'
else
	echo 'Exit.'
	echo 'Please, run this file again to configure your collector.'
fi