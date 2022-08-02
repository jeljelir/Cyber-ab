# CyberLab
A pentest academy

## Install Modules
```bash
sudo pip install requirements.txt 
sudo apt install nmap
sudo apt install wapiti
sudo pip install sslyze
```

## Setup Certificate
```bash
sudo apt install python3-acme python3-certbot python3-mock python3-openssl python3-pkg-resources python3-pyparsing python3-zope.interface
sudo apt install python3-certbot-nginx

#
sudo nano /etc/nginx/sites-available/domain.tld

# verify the syntax of the nginx configuration
sudo nginx -t && sudo systemctl reload nginx

# get the firewall status
sudo ufw status

# allow nginx HTTP and HTTPS
sudo ufw allow 'Nginx Full'

# setup the certificate
sudo certbot --nginx -d domain.tld -d www.domain.tld
```

### Setup Ngnix for SSL and Redicrections
Edit the `/etc/nginx/sites-enabled/domain.ltd` as follows.
```bash
erver {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name  domain.ltd www.domain.ltd;
    root   /path/to/webapp;

    ssl_certificate /etc/letsencrypt/live/domain.ltd/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/domain.ltd/privkey.pem; # managed by Certbot

    return 301 https://www.domain.ltd:5000$request_uri;
    client_max_body_size 100M;

    autoindex off;
}

server {
    listen 80;
    listen [::]:80;

    server_name  domain.ltd www.domain.ltd;
    return 301 https://www.domain.ltd:5000$request_uri;
}
```
And finally check if Nginx is formatted correctly by 'sudo nginx -t'.

## Run the App
Setup some Flask variables for the first time. No need to do it every time.
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
```

And run the app. It should be run in the webapp folder.
```bash
sudo gunicorn --certfile /etc/letsencrypt/live/domain.tld/fullchain.pem --keyfile /etc/letsencrypt/live/domain.tld/privkey.pem  --bind 0.0.0.0:5000 app:app
```
