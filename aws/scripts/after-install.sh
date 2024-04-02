#!/bin/bash

if [ "$DEPLOYMENT_GROUP_NAME" == "AttackerDeployment" ]
then
    cp -R /tmp/files/attacker /home/ec2-user
    rm -rf /tmp/files
fi


if [ "$DEPLOYMENT_GROUP_NAME" == "VictimDeployment" ]
then
    cp -R /tmp/files/victim /home/ec2-user
    rm -rf /tmp/files

    SERVER_IP=$(curl https://checkip.amazonaws.com)

    cat > /etc/httpd/conf.d/vhost.conf <<EOF
    <VirtualHost *:80>
        ServerName ${SERVER_IP}

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/
    </VirtualHost>

    EOF
fi
