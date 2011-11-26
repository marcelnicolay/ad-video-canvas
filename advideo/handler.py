import os
import json
import time
import base64

from tornado import gen, web
from pyiqe import Api

from advideo.buscape import Vitrine
from advideo.image_processing import calc_hash
from advideo.cache import Memcached

class DemoHandler(web.RequestHandler):
    pass
class FindAdHandler(web.RequestHandler):
    
    @web.asynchronous
    @gen.engine
    def get(self):
        vitrine = yield gen.Task(Vitrine().getByKeyword, "Apple iphone")
        self.write("Hello, world")

class ImgProcHandler(web.RequestHandler):

    def _get_keyword(self):
        
        IQE_KEY = '0e640412a82a4896bfb40bb53429729b'
        IQE_SECRET = '310970e406d94f9db24b2c527d7ae6d9'

        cache = Memcached(["localhost:11211"], 60)

        #file_image = self.request.files['']
        hash_value = calc_hash(self.request.body)
        keyword = cache.get(hash_value)
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
            
            keyword = " ".join(results)
            
            cache.set(hash_value, keyword)
        
        return keyword

    @web.asynchronous
    @gen.engine
    def post(self):
        
        keyword = self._get_keyword()
        vitrine = yield gen.Task(Vitrine().getByKeyword, keyword)

        response = {
            'vitrine': vitrine.as_dict()
        }
        
        self.set_header('Content-type', 'application/json; charset=utf-8')
        self.write(json.dumps(response))
        self.finish()
        
    def get(self):
        tpl = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload.html')
        self.write(open(tpl).read())
