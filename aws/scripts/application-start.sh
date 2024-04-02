#!/bin/bash

if [ "$DEPLOYMENT_GROUP_NAME" == "AttackerDeployment" ]
then
    echo "attacker deployment"
fi


if [ "$DEPLOYMENT_GROUP_NAME" == "VictimDeployment" ]
then
    cd /home/ec2-user/victim

    ./mvnw package
    nohup java -jar target/demo-0.0.1-SNAPSHOT.jar & echo $! > ./pid.file &

    service httpd start
fi
