from tornado import web
from tornado import gen
from advideo.buscape import Vitrine

class FindAdHandler(web.RequestHandler):

    @web.asynchronous
    @gen.engine
    def get(self):
        
        vitrine = yield gen.Task(Vitrine().getByKeyword, "Apple iphone")
        import pdb;pdb.set_trace()
        self.write("Hello, world")

