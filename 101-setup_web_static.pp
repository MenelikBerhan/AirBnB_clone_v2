# Set up my webservers for web server use

exec { 'update_and_install_nginx':
  command => 'apt-get update; apt-get -y install nginx',
  provider => shell
}
-> exec {'create_folders':
command  => 'mkdir -p /data/web_static/shared; mkdir -p /data/web_static/releases/test; ',
provider => shell
}
-> exec {'create_test_index':
command  => 'echo "Menelik Berhan" > /data/web_static/releases/test/index.html',
provider => shell
}
-> exec {'symbolic_link-change_owner':
command  => 'ln -sf /data/web_static/releases/test /data/web_static/current; chown -R ubuntu:ubuntu /data/;',
provider => shell
}
-> exec {'config_nginx':
command => 'sudo sed -i "s/server_name _;/server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}|" /etc/nginx/sites-enabled/default',
provider => shell
}
-> exec {'restart_nginx':
command  => 'sudo service nginx restart',
provider => shell
}
