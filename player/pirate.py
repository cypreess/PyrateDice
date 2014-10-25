#!/usr/bin/env python

import argparse
import json
import sys
import cherrypy

class Pirate(object):
    @cherrypy.expose
    def ping(self):
        return "pong\n"

    @cherrypy.expose
    def error(self, message):
        print >> sys.stderr, "ERROR MESSAGE FROM SERVER: %s" % message
        return "OK\n"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def bid(self):
        data = cherrypy.request.json
        return json.dumps(self.do_bid(data))

    def do_bid(self, data):
        raise NotImplementedError()


    def get_argparser(self):
        parser = argparse.ArgumentParser(description='Runs yours pirate.')
        parser.add_argument('--port', default=8000, type=int, help='tcp port')
        parser.add_argument('--host', default='0.0.0.0', help='hostname ip')
        return parser

    def run(self):
        self.args = self.get_argparser().parse_args()
        cherrypy.quickstart(self, config={
            'global': {
                'server.socket_port': self.args.port,
                'server.socket_host': self.args.host
            }
        })


if __name__ == '__main__':
    Pirate().run()
