#!/bin/bash

if [ "$DEPLOYMENT_GROUP_NAME" == "AttackerDeployment" ]
then
    echo "attacker deployment"
fi


if [ "$DEPLOYMENT_GROUP_NAME" == "VictimDeployment" ]
then
    cd /home/ec2-user/victim

    ./stop.sh

    isExistApp=`pgrep httpd`
    if [[ -n  $isExistApp ]]
    then
        service httpd stop
    fi
fi
