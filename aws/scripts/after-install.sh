#!/bin/bash

if [ "$DEPLOYMENT_GROUP_NAME" == "AttackerDeployment" ]
then
    cp -R /tmp/files/attacker /home/ec2-user
    rm -rf /tmp/files

    # install requirements
    source /home/ec2-user/venv/bin/activate

    python -m pip install -r /home/ec2-user/attacker/requirements.txt

    # create helper scripts
    cd /home/ec2-user/attacker

    SERVER_IP=$(curl https://checkip.amazonaws.com)

    cat > ./start_attack.sh <<-EOF
	python poc.py --userip ${SERVER_IP} --webport 8000 --lport 9001

	EOF

    cat > ./listen.sh <<-EOF
	ncat -lvnp 9001

	EOF

    # update permissions
    chmod -R 755 /home/ec2-user
    chown -R ec2-user:ec2-user /home/ec2-user
fi


if [ "$DEPLOYMENT_GROUP_NAME" == "VictimDeployment" ]
then
    cp -R /tmp/files/victim /home/ec2-user
    rm -rf /tmp/files

    # configure httpd to serve spring boot application
    SERVER_IP=$(curl https://checkip.amazonaws.com)

    cat > /etc/httpd/conf.d/vhost.conf <<-EOF
	<VirtualHost *:80>
	    ServerName ${SERVER_IP}

	    ProxyPreserveHost On
	    ProxyPass / http://localhost:8080/
	    ProxyPassReverse / http://localhost:8080/
	</VirtualHost>

	EOF

    cd /home/ec2-user/victim

    # create helper scripts to start and stop spring boot application
    cat > ./start.sh <<-EOF
	java -jar target/demo-0.0.1-SNAPSHOT.jar & echo \$! > ./pid.file &

	EOF

    cat > ./stop.sh <<-EOF
	kill \$(cat ./pid.file)

	EOF

    cat > ./start_silent.sh <<-EOF
	nohup ./start.sh > foo.out 2> foo.err < /dev/null &

	EOF

    # update permissions
    chmod -R 755 /home/ec2-user
    chown -R ec2-user:ec2-user /home/ec2-user
fi
