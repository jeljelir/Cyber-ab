[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

# CyberLab
CyberLab is a pentest academy for beginner pentester who like to learn basics.


To run CyberLab Pentest Academy, the following steps need to be taken:
1. Prepare a server
2. Install needed packages
3. Configure the server (network/firewall)
4. Set up DNS
5. Configure the webserver
6. Set up an SSL certificate
7. Run the web app

# 1. Prepare Sever
The first thing is to have a server. You can have a virtualized server or a VPS in your home lab. CyberLab has been tested on Debian 10 and 12 but should also work perfectly on other operating systems.
## VPS Server
In this case, the service provider will provide you with several OS options, usually including Debian. Just select one and proceed with the OS installation.
## Home Lab
You can have different virtualization setups: VMware, VirtualBox, Proxmox, etc. You can just set up your virtualization and install Debian. If you do not know how to install Debian, here is a [video instruction](https://youtu.be/bB-gmnvYDao).

# 2. Install Packages
When the server is up and ready, you can log in through SSH (or VNC) and install the needed packages and tools.
## 2.1. Update and Upgrade
The first thing is to update and upgrade existing packages, which can be done by running commands as follows.
```bash
sudo apt update && sudo apt upgrade
```
## 2.2. Python and PIP
Python PIP should be installed by default, but in this case, it could be installed by the following code
```bash
sudo apt install python3 python3-pip
```
## 2.3. Flask, Gunicorn, and Flask-Session
Flask is a web framework for Python that lets us develop web apps with Python. Flask-Session is a Flask extension that enables the server side sessions. Gunicorn is a WSGI HTTP Server for UNIX that helps us run our developed web app on a Linux server.

To install these packages, run the following command. If you want to install it for the current user, add the `--user` argument to the command.
```bash
pip install -r requirements.txt
```

## 2.4. Pentest Tools
CyberLab includes three pentest tools that need to be installed on the server. Here are the commands to install them.
```bash
sudo apt install nmap
sudo apt install wapiti
sudo pip install sslyze
```

## 2.5. Webserver and Firewall
First, let's install a firewall package. I prefer UFW as it is simple and effective.
```bash
sudo apt install ufw
```
As we need a web server, I prefer to use Nginx, which works better with Flask.
```bash
sudo apt install nginx
```

## 2.6. GIT
To be able to clone CyberLab from its Github repository, we need to install `git` by running the following command.
```bash
sudo apt install git
```

# 3. Server Configuration
To access the web app from the Internet, we need to set up the firewall and ensure the networking is set up correctly. By finishing this step, you should be able to access your server by visiting `http://your_public_ip` on your browser or via terminal by `curl http://your_public_ip`.

## 3.1. Firewall
We need access to some ports, including `80`, `443`, `5000`, and `22`. These ports are blocked by default and need to be opened by setting up some firewall rules. UFW has app bundles that can be seen by running `sudo ufw app list`; for this purpose, we are more interested in `Nginx Full` as well as two other ports (`22` for SSH and `5000` as our web app can adequately work on the ports `80` or `443`).

To set up firewall rules, run the following command.
```bash
sudo ufw allow 'Nginx HTTP',SSH,5000
```

We can see the result by running the following command.
```bash
sudo ufw status
```

## 3.2. Network Setup
If you run the web app on a VPS, you can ignore this section. If you have a home lab, you need to allow ports on your firewall (modem), too. The instructions differ based on the brand of the modem and/or firewall. Just google how you can `open ports on [brand_of_your_modem]` or log in to the modem management and look for port forwarding. Here, you need to tell what port on which device should be opened.

In the screenshot below, I set up the port `80` on my router to be open for the device `192.110.12.100`. You need to do the same for ports `443`, `5000`, and `22`.

![Port Forwarding on TP-Link](img/port-forwardning.png)

The device is usually defined by its IP address. If you do not know how to get your server's IP address, just run `ip addr` on Linux or `ipconfig` on Windows.


# 4. DNS and DDNS
As we probably need to set up basic DNS for a domain we would like to show our webapp on, I use Cloudflare. If you are in your home lab, you can set up a [Dynamic DNS](https://github.com/namnamir/configurations-and-security-hardening/blob/main/DDNS.md).

I would like to have a setup like this:
```
sub.domain.ltd -> public_ip_v4
sub.domain.ltd -> public_ip_v6
```
To do so, we need to set up `A` and `AAAA` DNS records for the desired subdomain. Here, you can see my setup. Keep in mind that if you use a home lab, you need to turn off the proxy (the orange sign beside `Proxied`).
![DNS Setup on Cloudflare](img/cloud-flare.png)

# 5. Webserver Configuration
Now that we have pointed our domain to our IP, it is time to set up our web server to understand our domain. After finishing this step, you should be able to access your server by visiting `http://domain.tld` on your browser or via terminal by `curl http://domain.tld`.

First, you need to create a config file for your domain in `/etc/ngnix/sites-available` by `sudo nano /etc/nginx/sites-available/domain.tld` and add the following lines.
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name  domain.ltd www.domain.ltd;
    root /path/to/webapp;
}
```
After saving changes, we can check the configuration by `sudo nginx -t`. If everything is `ok`, we can restart the Nginx service by `sudo service nginx restart` or `sudo systemctl reload nginx` to apply our changes.

# 6. Setup Certificate
By having LetsEncrypt on the server, we can install the certificate for our web app. To do so, run the following command.  By finishing this step, you should be able to access your server on SSL by visiting `https://domain.tld` on your browser or via terminal by `curl https://domain.tld`.
```bash
sudo certbot --nginx -d domain.tld -d www.domain.tld -d sundomain.domain.tld
```

## Reconfigure Ngnix Config File
As I use a subdomain `sundomain.domain.tld`, and as I like to redirect ports `443` and `80` to `5000`, I need to make some changes to the config file. So, I open `/etc/nginx/sites-enabled/domain.ltd` and edit it as follows.
```bash
erver {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name domain.ltd www.domain.ltd www.domain.tld;
    root /path/to/webapp;

    ssl_certificate /etc/letsencrypt/live/domain.ltd/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/domain.ltd/privkey.pem; # managed by Certbot

    # redirect https to port 5000
    return 301 https://www.domain.ltd:5000$request_uri;
    client_max_body_size 100M;

    autoindex off;
}

server {
    listen 80;
    listen [::]:80;

    server_name  domain.ltd www.domain.ltd sundomain.domain.tld;
    
    # redirect http to https port 5000
    return 301 https://www.domain.ltd:5000$request_uri;
}
```
Again, check if Nginx is formatted correctly by 'sudo nginx—t' and restart it by `sudo service nginx restart` or `sudo systemctl reload nginx`.

# 7. Lunching WebApp
Everything seems fine. We just need to clone the web app on our server and run it.

## Clone the WebApp
To clone the webapp, go the path you like to clone the webapp and run the following command.
```bash
git clone https://github.com/jeljelir/CyberLab.git
```

## Set Uo Flask Variables
Set up some Flask variables for the first time. There is no need to do it every time.
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## Run it
And the very last step is to go to the `CyberLab` folder and run the app by this command.
```bash
sudo gunicorn --certfile /etc/letsencrypt/live/domain.tld/fullchain.pem --keyfile /etc/letsencrypt/live/domain.tld/privkey.pem --bind 0.0.0.0:5000 app:app
```
Now, you should be able to open the website by visiting `https://<domain.tld>:5000`.
