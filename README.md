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

## Run the App
```bash
# Linux
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Windows
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = development
$env:LASK_DEBUG = 1
```
```bash
sudo gunicorn --certfile /etc/letsencrypt/live/domain.tld/fullchain.pem --keyfile /etc/letsencrypt/live/domain.tld/privkey.pem  --bind 0.0.0.0:5000 app:app
```
