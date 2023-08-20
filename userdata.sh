#!/bin/bash
yum update -y
yum install httpd -y
systemctl enable httpd
systemctl start httpd
echo "<h1>Hola CDK, soy la instancia $(curl http://169.254.169.254/latest/meta-data/instance-id)</h1>" > /var/www/html/index.html
