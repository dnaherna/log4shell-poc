#!/bin/bash

if [ "$DEPLOYMENT_GROUP_NAME" == "AttackerDeployment" ]
then
    echo "attacker deployment"
fi


if [ "$DEPLOYMENT_GROUP_NAME" == "VictimDeployment" ]
then
    cd /home/ec2-user/victim

    ./mvnw package

    ./start_silent.sh

    service httpd start
fi
