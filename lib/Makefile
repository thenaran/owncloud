install:
	@mkdir -p /var/www/owncloud
	-@if ! [ -f /lib/owncloud-6.0.2.tar.bz2 ]; then wget http://download.owncloud.org/community/owncloud-6.0.2.tar.bz2 /lib/owncloud-6.0.2.tar.bz2; fi
	@cp -f /lib/nginx-default /etc/nginx/nginx.conf
	@openssl req -new -x509 -days 365 -nodes -out /etc/nginx/cert.pem -keyout /etc/nginx/cert.key -subj /C=KR/ST=Seoul/L=Seoul/O=Naran/OU=IT/CN=localhost
	@chmod 644 /etc/nginx/cert.pem
	@chmod 644 /etc/nginx/cert.key
	@sed /etc/php5/fpm/pool.d/www.conf -i -e "s|listen = /var/run/php5-fpm.sock|listen = 127.0.0.1:9000|g"
	@mv /lib/owncloud-6.0.2.tar.bz2 /var/www/
	@cd /var/www; tar xjf owncloud-6.0.2.tar.bz2; rm owncloud-6.0.2.tar.bz2
	@chown -R www-data:www-data /var/www
	@chmod -R 777 /var/www
	@chmod -R 777 /var/lib/nginx
	@chmod -R 777 /var/log/nginx
	@/etc/init.d/nginx stop
	@/etc/init.d/php5-fpm stop
	@sed -i s/Sameorigin/None/g /var/www/owncloud/lib/private/template.php
	@cp -f /lib/locale.gen /etc/locale.gen
	@locale-gen
	@chown -R www-data /usr/share/zoneinfo/*
	@cp -f /lib/php.ini /etc/php5/fpm/php.ini
	@cp -f /lib/htaccess /var/www/owncloud/.htaccess
	@find /lib/owncloud -exec touch -c -h -m -t 201401010000 {} \;
