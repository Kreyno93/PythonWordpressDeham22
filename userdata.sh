#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras enable php8.0
sudo amazon-linux-extras install -y php8.0
sudo yum install -y httpd mariadb
sudo systemctl start httpd
sudo systemctl enable httpd
cd /var/www/html
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cp -r wordpress/* .
rm -rf wordpress latest.tar.gz
chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html
systemctl restart httpd