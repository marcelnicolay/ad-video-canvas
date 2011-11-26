# coding: utf-8
#!/usr/bin/env python

from tornado.httpclient import AsyncHTTPClient
from tornado.options import options
import logging
import json
import urllib
import httplib
import functools

from advideo.image_processing import calc_hash
from advideo.cache import Memcached

from tornado import gen

class Vitrine(object):

    def __init__(self, produto_id=None, source_id=None):
        self.produto_id = produto_id
        self.source_id = source_id

    def as_dict(self):
    
        return { 'name':self.name, 'produto_id': self.produto_id, 'pricemin':self.pricemin, 'thumb': self.buscape_image_url, 'compare': self.compare }

    @gen.engine
    def getByKeyword(self, keyword, callback):
    
        cache = Memcached(["localhost:11211"], 60)

        hash_value = calc_hash("getbykeyword:keyword")
        vitrine = cache.get(hash_value)
        
        if not vitrine:
            produto_buscape = yield gen.Task(Produto.getProductByName, keyword)
            
            if not produto_buscape:
                produto_buscape = yield gen.Task(Produto.getTopProduct)
    
            vitrine = Vitrine().getByProdutoBuscape(
                produto_id = produto_buscape['id'],
                buscape_image_url = produto_buscape['thumbnail']['url'],
                name = produto_buscape['productname'].encode("utf-8"),
                pricemin = produto_buscape.get('pricemin'),
                pricemax = produto_buscape.get('pricemax'),
                compare = [link['link']['url'] for link in produto_buscape.get('links') if link['link']['type'] == 'product'][0],
            )
            cache.set(hash_value, vitrine)
            
        callback(vitrine)

    def getByProdutoBuscape(self, produto_id, buscape_image_url, name, pricemin, pricemax, compare):

        vitrine = Vitrine()
        vitrine.produto_id = produto_id
        vitrine.buscape_image_url = buscape_image_url
        vitrine.name = name
        vitrine.pricemin = pricemin
        vitrine.pricemax = pricemax
        vitrine.compare = compare

        return vitrine
        
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
        else:
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