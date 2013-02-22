import os

NGINX_CWD = os.path.join("C:\\", "opt", "nginx")
NGINX_EXECUTABLE = os.path.join(NGINX_CWD, "nginx.exe")
NGINX_CONF = os.path.join(NGINX_CWD, "conf", "nginx.conf")

PHP_CWD = os.path.join("C:\\", "opt", "php-5.4")
PHP_EXECUTABLE = os.path.join(PHP_CWD, "php-cgi.exe")
PHP_INI = os.path.join(PHP_CWD, "php.ini")

MONGODB_CWD = os.path.join("E:\\", "bin", "srv", "mongodb")
MONGODB_EXECUTABLE = os.path.join(MONGODB_CWD, "bin", "mongod.exe")
MONGODB_CLIENT_EXECUTABLE = os.path.join(MONGODB_CWD, "bin", "mongo.exe")
MONGODB_CONF = os.path.join(MONGODB_CWD, "mongodb.conf")

MYSQL_CWD = os.path.join("C:\\", "opt", "mysql")
MYSQLD_EXECUTABLE = os.path.join(MYSQL_CWD, "bin", "mysqld.exe")
MYSQLADMIN_EXECUTABLE = os.path.join(MYSQL_CWD, "bin", "mysqladmin.exe")
MYSQLADMIN_PARAMS = ['--host', '127.0.0.1', '--user', 'root']
MYSQL_CONF = os.path.join(MYSQL_CWD, "bin", "my.ini")

REDIS_CWD = os.path.join("C:\\", "opt", "redis")
REDIS_SERVER_EXECUTABLE = os.path.join(REDIS_CWD, 'redis-server.exe')
REDIS_CLI_EXECUTABLE = os.path.join(REDIS_CWD, 'redis-cli.exe')
REDIS_CLI_PARAMS = ['-h', '127.0.0.1']

MONGODB_PERIODICALLY_TOUCH_DB_FILES = True

START_NGINX = True
START_PHP = True
START_MONGODB = True
START_MYSQL = True
START_REDIS = True
