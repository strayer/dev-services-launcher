# coding=utf-8
import subprocess
import os
import sys

from pyparsing import Word, nums, Combine, alphas, alphanums, Suppress, Keyword, OneOrMore, Group, ParseException

class Nginx(object):
    def __init__(self, nginx_path):
        self.path = nginx_path
        self.config_path = os.path.join(self.path, "conf", "nginx.conf")
        self.upstreams = {}

        if not os.path.exists(self.config_path):
            sys.exit("Could not find nginx config at path "+self.config_path)

        self.nginx_config = open(self.config_path).read()

        self.parse_upstreams()

        if not self.upstreams.__contains__('php'):
            sys.exit("Could not find upstream php in nginx config")

    def start(self):
        self.process = subprocess.Popen(
            args = [os.path.join(self.path, "nginx.exe")],
            cwd = self.path
        )

    def stop(self,):
        stop_process = subprocess.Popen(
            args = [os.path.join(self.path, "nginx.exe"), '-s', 'quit'],
            cwd = self.path
        )

        self.process.wait()
        stop_process.wait()

    def reload_config(self):
        reload_process = subprocess.Popen(
            args = [os.path.join(self.path, "nginx.exe"), '-s', 'reload'],
            cwd = self.path
        )

        reload_process.wait()

    def __str__(self):
        args = [os.path.join(self.path, "nginx.exe"), '-v']

        proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        stderr = stderr.replace(b'nginx version: ', b'')

        return stderr.strip().decode('utf-8')

    def get_php_upstream(self):
        return self.upstreams.get("php")

    def parse_upstreams(self):
        # function to create range validation parse actions
        def validInRange(lo, hi):
            def parseAction(tokens):
                if not lo <= int(tokens[0]) <= hi:
                    raise ParseException("", 0, "integer outside range %d-%d" % (lo, hi))

            return parseAction

        # define basic building blocks
        integer = Word(nums)
        ip_int = integer.copy().setParseAction(validInRange(0, 255))
        ip_addr = Combine(ip_int + ('.' + ip_int) * 3)
        ip_port = integer.copy().setParseAction(validInRange(1025, 65535))
        ip_addr_port = ip_addr("ip_addr") + ':' + ip_port("ip_port")
        ident = Word(alphas, alphanums + "_")

        # define punctuation needed — but use Suppress so it does
        # not clutter up the output tokens
        SEMI, LBRACE, RBRACE = map(Suppress, ";{}")

        # define a server entry that will be found in each upstream block
        server_def = Keyword("server") + ip_addr_port + SEMI

        # define an upstream block
        upstream_block = Keyword("upstream") + ident("stream_id") +\
                         LBRACE + OneOrMore(Group(server_def))("servers") + RBRACE

        # now scan through the string containing the nginx config
        # data, extract the upstream blocks and their corresponding
        # server definitions — access tokens using results names as
        # specified when defining server_def and upstream_block
        for usb in upstream_block.searchString(self.nginx_config):
            upstream = []
            for server in usb.servers:
                upstream.append(server.ip_addr+":"+server.ip_port)
            self.upstreams[usb.stream_id] = upstream