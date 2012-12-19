import os

NGINX_CWD = os.path.join('C:\\', 'opt', 'nginx')
NGINX_EXECUTABLE = os.path.join(NGINX_CWD, 'nginx.exe')
NGINX_CONF = os.path.join(NGINX_CWD, 'conf', 'nginx.conf')
PHP_CWD = os.path.join('C:\\', 'opt', 'php-5.4')
PHP_EXECUTABLE = os.path.join(PHP_CWD, 'php-cgi.exe')
PHP_INI = os.path.join(PHP_CWD, 'php.ini')

START_NGINX = True
START_PHP = True
