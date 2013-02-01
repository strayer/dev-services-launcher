#!/usr/bin/python3
# coding=utf-8
from services import Nginx, NginxConfigException, PHP, MongoDB
import tools
import settings

nginx = Nginx()
nginx_upstreams = None
try:
    nginx_upstreams = nginx.get_php_upstream()
except NginxConfigException:
    pass
php = PHP(nginx_upstreams)
mongodb = MongoDB()

if settings.START_PHP:
    print("PHP version: {}".format(php))
if settings.START_NGINX:
    print("Nginx version: {}".format(nginx))
if settings.START_MONGODB:
    print("MongoDB version: {}".format(mongodb))

print("")

stop_execution = False

if settings.START_PHP:
    print("Starting PHP ({} instances)".format(len(php.addresses)))
    php.start()
if settings.START_NGINX:
    print("Starting Nginx")
    nginx.start()
if settings.START_MONGODB:
    print("Starting MongoDB")
    mongodb.start()

print("")
print("Menu:")
if settings.START_NGINX:
    print("(r) to reload Nginx config")
if settings.START_PHP:
    print("(p) to restart PHP processes")
print("---")
print("(STRG+c) or (q) to quit")
print("")

while True:
    char = tools.getch()

    if char == b"\x03" or char == b"q":
        break
    elif char == b"r" and settings.START_NGINX:
        print("Reloading Nginx config... ",end="")
        nginx.reload_config()
        print("done")
    elif char == b"p" and settings.START_PHP:
        print("Restarting PHP processes... ",end="")
        php.stop()
        php.start()
        print("done")

print("Stopping processes...")
if settings.START_NGINX:
    nginx.stop()
if settings.START_PHP:
    php.stop()
if settings.START_MONGODB:
    mongodb.stop()
