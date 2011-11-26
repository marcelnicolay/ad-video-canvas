# coding: utf-8
#!/usr/bin/env python

from tornado.httpclient import AsyncHTTPClient
from tornado.options import options
import logging
import json
import urllib
import httplib
import functools

from advideo import imaging
from tornado import gen




class Vitrine(object):

    def __init__(self, produto_id=None, source_id=None):
        self.produto_id = produto_id
        self.source_id = source_id

    def as_dict(self):
    
        return { 'url':self.url, 'name':self.name, 'produto_id': self.produto_id }

    @gen.engine
    def getByKeyword(self, keyword, callback):
    
        produto_buscape = yield gen.Task(Produto.getProductByName, keyword)
        import pdb;pdb.set_trace()
        
        if not produto_buscape:
            produto_buscape = yield gen.Task(Produto.getTopProduct)
    
        vitrine = Vitrine().getByProdutoBuscape(
            produto_id = produto_buscape['id'],
            buscape_image_url = produto_buscape['thumbnail']['url'],
            name = produto_buscape['productname'].encode("utf-8"),
            pricemin = produto_buscape.get('pricemin'),
            pricemax = produto_buscape.get('pricemax')
        )
        import pdb;pdb.set_trace()
        callback(vitrine)


    def getByProdutoBuscape(self, produto_id, buscape_image_url, name, pricemin, pricemax):

        vitrine = Vitrine()
        vitrine.produto_id = produto_id
        vitrine.buscape_image_url = buscape_image_url
        vitrine.name = name
        vitrine.pricemin = pricemin
        vitrine.pricemax = pricemax

        # create vitrine
        vitrine.create()

        return vitrine
    
    def create(self):
    
        try:
        
            title = self.name
    
            image_name = imaging.ComposeImage.compose(image_url=self.buscape_image_url, image_path=options.IMAGE_PATH, title=title, price= (self.pricemin, self.pricemax) )
    
            self.url = "%s/%s" % (options.IMAGE_URL, image_name)
        except:
            logging.exception("falha ao criar a imagem de vitrine %s, %s, %s" % (self.buscape_image_url, options.IMAGE_PATH, title ))
        
            raise ValueError("Falha ao criar a imagem")
        
class Produto(object):
	
    @staticmethod
    @gen.engine
    def findProductList(keyword, results=1, callback=None):

        url_produto = options.BUSCAPE_API_URL % { 'service': 'findProductList', 'application_id': options.BUSCAPE_API_ID}

        url_produto += "?"+ "&".join(["keyword=%s" % urllib.quote(keyword), "format=json", "results=%s" % results ])

        logging.info("[Buscape] findProductList %s..." % url_produto)

        http_client = AsyncHTTPClient()
        response = yield gen.Task(http_client.fetch, url_produto)
        
        if response.code == 200 and response.body:
            callback(json.loads(response.body))
        else:
            callback(None)
        
    @staticmethod
    @gen.engine
    def getProductByName(name, callback):
        
        product_list = yield gen.Task(Produto.findProductList, name)
        
        if product_list and product_list.has_key('product'):    		
            callback(product_list['product'][0]['product'])

        logging.info("produto %s nao encontrado no buscape" % name)
    
        callback(product_list)
        
    @staticmethod
    @gen.engine
    def getTopProduct(callback):
        url_produto = options.BUSCAPE_API_URL % { 'service': 'topProducts', 'application_id': options.BUSCAPE_API_ID}
        url_produto += "?"+ "&".join(["format=json", "results=1"])

        logging.info("[Buscape] getTopProduct %s..." % url_produto)

        http_client = AsyncHTTPClient()
        response = yield gen.Task(http_client.fetch, url_produto)
        
        product_list = None
        if response.code == 200 and response.body:
            product_list = json.loads(response.body)

        if product_list and product_list.has_key('product'):    		
            callback(product_list['product'][0]['product'])
        else:
            callback(None)