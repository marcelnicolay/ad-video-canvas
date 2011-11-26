# coding: utf-8

import os, sys, atexit, getopt
import tornado.web
import tornado.wsgi
import tornado.options
import tornado.ioloop
import logging
import wsgiref.simple_server

#def main():

tornado.options.define("BUSCAPE_API_ID", default="6a71545654426b56542b453d", help="")
tornado.options.define("BUSCAPE_API_URL", default="http://bws.buscape.com/service/%(service)s/%(application_id)s/", help="")
tornado.options.define("FONTS_DIR", default="%s/static/fonts/" % os.path.abspath(os.path.dirname(__file__)))
tornado.options.define("IMAGE_PATH", default="%s/../media/img/" % os.path.abspath(os.path.dirname(__file__)))
#tornado.options.define("IMAGE_URL", default="http://localhost:8888/media/img/produtos")
tornado.options.define("IMAGE_URL", default="http://dejavu-x.herokuapp.com/media/img/produtos")

#tornado.options.parse_command_line()        

# settings, path.insert
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath("%s/.." % project_root))

logging.getLogger().setLevel(getattr(logging, tornado.options.options.logging.upper())) 

from advideo.handler import FindAdHandler, ImgProcHandler

application = tornado.web.Application([
    (r"/", ImgProcHandler),
    (r"/findad", FindAdHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
])

if __name__ == "__main__":

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


