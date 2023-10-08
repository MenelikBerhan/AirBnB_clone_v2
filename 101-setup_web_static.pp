# Set up my webservers for web server use
$config_text="server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name _;
	location /hbnb_static {
		alias /data/web_static/current/;
	}

	add_header X-Served-By \$hostname;	

	location / {
		try_files \$uri \$uri/ =404;
	}

	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
	}

	error_page 404 /404.html;
	location /404.html {
		internal;
	}
}"
$test_content="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>\n"
$err_content="Ceci n'est pas une page\n"
$default_content="Holberton School\n"

exec { 'update_and_install_nginx':
  command  => 'apt-get update; apt-get -y install nginx',
  provider => shell
}
-> exec {'create_folders':
command  => 'mkdir -p /data/web_static/shared; mkdir -p /data/web_static/releases/test; ',
provider => shell
}
-> file {'create_test_index':
path    => '/data/web_static/releases/test/index.html',
content => $test_content
}
-> file {'nginx_config':
  path    =>  '/etc/nginx/sites-available/default',
  content => $config_text
}
-> file {'index_html':
  path    =>  '/var/www/html/index.html',
  content => $default_content
}
-> file {'404_html':
  path    =>  '/var/www/html/404.html',
  content => $err_content
}
-> exec {'symbolic_link_change_owner':
command  => 'ln -sf /data/web_static/releases/test /data/web_static/current; chown -R ubuntu:ubuntu /data/;',
provider => shell
}
-> exec {'restart_nginx':
command  => 'sudo service nginx restart',
provider => shell
}
