#/bin/bash
# The command above states wich shell is used

# This file is used to set up the project installing all requirements and dependencies
# Keep it as automated as possible, as the software must be easy enough for everyone to install
# Use ----- <Description> ----- to help users track installation proccess and possible errors.

# Every step is divided in sections as the following, so it is easier to track error and program

echo "************************************************************"
echo "| The installation of the RadarLivre Collector has just    |"
echo "| begun.                                                   |"
echo "| Note that you need a running server in order to get data |"
echo "| from your collector.                                     |"
echo "| This setup will help you configure your collector and    |"
echo "| make it functional.                                      |"
echo "| This may take several minutes. Please, be patient.       |"
echo "************************************************************"

echo "************************************************************"
echo "| Updating apt-get                                         |"
echo "************************************************************"

sudo apt-get update -y
sudo apt-get upgrade -y