#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static

# Update and install nginx if it's not already installed
sudo apt update
sudo apt install -y nginx

# Create the folders, if they don't yet exist
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML file '/data/web_static/releases/test/index.html'
echo "<html>
  <head>
  </head>
  <body>
    Hello to Web Static
  </body>
</html>" >> /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -fs /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu's user and group
sudo chown -R ubuntu:ubuntu /data/

# Updating the Nginx configuration
loc_header="location \/hbnb\_static\/ {"
loc_content="alias \/data\/web\_static\/current\/;"
new_location="\n\t$loc_header\n\t\t$loc_content\n\t}\n"
sudo sed -i "37s/$/$new_location/" /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart