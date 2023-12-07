#!/bin/env bash
# Script that sets up a web servers for the deployment of web_static.

if ! [ -x "$(command -v nginx)" ]; then
apt update
apt-get - y install nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<h1>
Some random content for testing
</h1>" | tee /data/web_static/releases/test/index.html > /dev/null

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

bash -c 'cat << EOF > /etc/nginx/sites-available/web_static
server {
	listen 80;

	server_name samuelnandi.tech www.samuelnandi.tech;

    root /data/web_static/;
    index index.html index.htm index.nginx-debian.html;

    location / {
        try_files $uri $uri/ =404;
    }

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}
}
EOF'

ln -sf /etc/nginx/sites-available/web_static /etc/nginx/sites-enabled/

systemctl restart nginx
