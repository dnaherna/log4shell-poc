if [ "$DEPLOYMENT_GROUP_NAME" == "AttackerDeployment" ]
then
    cp -R /tmp/files/attacker /home/ec2-user
    rm -rf /tmp/files
fi


if [ "$DEPLOYMENT_GROUP_NAME" == "VictimDeployment" ]
then
    cp -R /tmp/files/victim /home/ec2-user
    rm -rf /tmp/files
fi
