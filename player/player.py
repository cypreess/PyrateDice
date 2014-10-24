#!/usr/bin/env python

import cherrypy

class Player:
    @cherrypy.expose
    def ping(self):
        return "pong\n"

    def move(self):
        return "move\n"

if __name__ == '__main__':
    cherrypy.quickstart(Player())
