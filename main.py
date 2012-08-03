# coding=utf-8
import os
import signal
import time

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

# catch SIGINT and tell the loop to stop
def signal_handler(signal, frame):
    global stop_execution
    print("Signal received")
    stop_execution = True

signal.signal(signal.SIGINT, signal_handler)

print("Starting PHP ({} instances)".format(len(php.addresses)))
php.start()
print("Starting Nginx")
nginx.start()

while not stop_execution:
    # An exception will be thrown when the signal_handler is executed while the sleep function is running.
    # Since we want it to stop anyways we can simply ignore it
    try:
        time.sleep(10)
    except IOError:
        pass

print("Stopping processes...")
nginx.stop()
php.stop()
