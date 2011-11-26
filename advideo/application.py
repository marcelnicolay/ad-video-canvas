import os
import json
import time
import base64

import tornado.ioloop
import tornado.web
from pyiqe import Api

from image_processing import calc_hash
from cache import Memcached

class FindAdHandler(tornado.web.RequestHandler):

    def post(self):
        IQE_KEY = '0e640412a82a4896bfb40bb53429729b'
        IQE_SECRET = '310970e406d94f9db24b2c527d7ae6d9'

        cache = Memcached(["localhost:11211"], 60)

        #file_image = self.request.files['']
        hash_value = calc_hash(self.request.body)
        cached_response = cache.get(hash_value)
        if not cached_response:
            file_image = '/tmp/%s.jpg' % hash_value
            open(file_image, 'w').write(self.request.body)

            api = Api(IQE_KEY, IQE_SECRET)
            data = api.query(file_image)
            response = api.update()

            name = response['data']['results'][0]['qid_data']['labels']
            results = []
            for res in response['data']['results']:
                data = {
                    'product_name': res['qid_data']['labels'],
                }
                results.append(data)
            response = {
                'results': results,
                'img_data': 'data:image/jpeg;base64,%s' % base64.b64encode(self.request.body),
            }
            cached_response = json.dumps(response)
            cache.set(hash_value, cached_response)

        self.set_header('Content-type', 'application/json; charset=utf-8')
        self.write(cached_response)

    def get(self):
        self.write(open('./upload.html').read())


application = tornado.web.Application([
    (r"/findad", FindAdHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()