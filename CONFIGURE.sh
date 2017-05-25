#/bin/bash
# The command above states wich shell is used

# This file is used to set up the project installing all requirements and dependencies
# Keep it as automated as possible, as the software must be easy enough for everyone to install
# Use ----- <Description> ----- to help users track installation proccess and possible errors.

# Every step is divided in sections as the following, so it is easier to track error and program

# Enter relative directory
BASEDIR=$(dirname "$0")
cd "$BASEDIR"


echo "************************************************************"
echo "| We are going to help you configure your collector now.   |"
echo "************************************************************"

echo "Please, provide your username:"
read username
echo "Please, provide your password:"
read password
echo "Please, enter your collector's ID(format: 12345678-1234-1234-1234-123456789012)"
read collectorID
echo "Please, enter where your server is located with the format 'http:\\path\to\your\server:port'."
echo "Leave blank if running a local server."
read serverHost

echo "Your username is $username."
echo "Your collector's ID is $collectorID."
echo "Your server is located at $serverHost."

read -p "Confirm?(y/n)" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Generating your configuration file."
else
	echo "Please, run CONFIGURE.sh again."
fi