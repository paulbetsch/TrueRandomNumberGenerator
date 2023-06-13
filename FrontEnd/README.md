# FrontEnd

## About

This Website can be used, to access the [API](../TRNG_API/__init__.py) in a user friendly way.

## Requirements
- Any Webserver you prefer, e. g. Apache or NGINX

## Installation
### Tutorial for NGINX Webserver:
1. run command: `sudo apt-get update && sudo apt-get upgrade`
2. run command: `sudo apt-get install nginx`
3. run command: `sudo cp -r . /var/www/`
4. edit the following file: `/etc/nginx/available-site/default`
5. change the contents of the above file to: 
```
server {
        listen 80;
        server_name $domain_name;
        root /var/www/FrontEnd;
        index index.html;
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
}
```
6. run command: `sudo service nginx restart`
7. Not you can access the Website via [http://localhost:80/](http://localhost:80)
8. __Be aware if you use an SSL Certificate change the configs and URLs__

## Scripts
- index.html: shows the form, which can be used to controll the API.
- scrip.js: sends the Requests to the API, when buttons are hit.
