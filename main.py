# coding=utf-8
import os
import tools

from Nginx import Nginx
from PHP import PHP

nginx_path = os.path.join('C:\\', 'opt', 'nginx')
php_path = os.path.join('C:\\', 'opt', 'php-5.4')

nginx = Nginx(nginx_path)
php = PHP(php_path, nginx.get_php_upstream())

print("PHP version: {}".format(php))
print("Nginx version: {}".format(nginx))
print('')

stop_execution = False

print("Starting PHP ({} instances)".format(len(php.addresses)))
php.start()
print("Starting Nginx")
nginx.start()

print("")
print("Menu:")
print("(STRG+c) or (q) to quit")
print("(r) to reload nginx config")
print("")

while True:
    char = tools.getch()

    if (char == b"\x03" or char == b"q"):
        break
    elif char == b"r":
        print("Reloading nginx config... ",end="")
        nginx.reload_config()
        print("done")
        print("")

print("Stopping processes...")
nginx.stop()
php.stop()
