#!/usr/bin/env bash
#  sets up my web servers for the deployment of web_static

# Create folders if they don't exist
if ! [ "$(command -v nginx)" ]; then
    sudo apt update;
    sudo apt install nginx -y;
fi
if ! [ -d "/data/" ]; then
    sudo mkdir /data/
fi
if ! [ -d "/data/web_static/" ]; then
    sudo mkdir /data/web_static/
fi
if ! [ -d "/data/web_static/releases/" ]; then
    sudo mkdir /data/web_static/releases/
fi
if ! [ -d "/data/web_static/shared/" ]; then
    sudo mkdir /data/web_static/shared/ 
fi
if ! [ -d "/data/web_static/releases/test/" ]; then
    sudo mkdir /data/web_static/releases/test/
fi

# Create a test html
echo "<html>
  <head>
  </head>
  <body>
    Menelik Berhan
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Change owner user and group of root folder /data
sudo chown -hR \"ubuntu\":\"ubuntu\" /data/

# Config nginx to serve hbnb_static if it hasn't been configured yet
insert="server_name _;\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}"
if ! ( sudo cat /etc/nginx/sites-available/default | grep -q hbnb_static); then
        sudo sed -i "s/server_name _;/$insert/" /etc/nginx/sites-available/default;
fi
sudo service nginx restart
