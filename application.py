import tornado.ioloop
import tornado.web

class FindAdHandler(tornado.web.RequestHandler):

    def post(self):
        
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/findad", FindAdHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()