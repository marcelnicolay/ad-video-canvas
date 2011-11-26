# coding: utf-8
#!/usr/bin/env python

import Image, ImageDraw, ImageFont, ImageOps
import cStringIO
import uuid
import urllib
import os

import logging

from tornado.options import options


class ComposeImage(object):

    @staticmethod
    def get_limited_text(text, limit):
        
        text_split = text.split(" ")
        text_limited = ""
        
        for word in text_split:
            
            if len(text_limited + word) > limit:
                break
                
            text_limited = " ".join([text_limited, word.strip()])
        
        return text_limited.strip()
            
    @staticmethod
    def compose(image_url, title, price, image_path):
        
        image_size = (320, 200)        
        
        font_dir = options.FONTS_DIR

        try:
            image_file = urllib.urlopen(image_url)
            
            if image_file.getcode() != 200:
                raise ValueError
                
            image_stream = cStringIO.StringIO(image_file.read())   
            image_produto = Image.open(image_stream)
            
        except:
            logging.error("Imaging falha ao recuperar a imagem %s" % image_url)
            image_produto = Image.open("%s/%s" % (image_path, "indisponivel_200.gif"))
        
        image_produto.thumbnail((100, 100), Image.ANTIALIAS)
#        image_produto_box = Image.new("RGBA", (102, 102), (0,0,0,0))
#        image_produto_box.paste(image_produto, (1,1))
        
        buscape_logo = Image.open("%s/%s" % (image_path, "buscape-logo-small.jpg"))
        
        image_name = "%s.jpg" % unicode(uuid.uuid5(uuid.NAMESPACE_DNS, str("%s%s" %(image_url,title))))
        image_file_name = "%s/%s" % (image_path, image_name)
        
        title_font = ImageFont.truetype(font_dir+"Verdana.ttf", 18, encoding='unic')
        label_font = ImageFont.truetype(font_dir+"Verdana.ttf", 12)
        price_font = ImageFont.truetype(font_dir+"Verdana Bold.ttf", 24)

        lineWidth = 20

        image_vitrine = Image.new('RGBA', image_size, (255,255,255, 255) )
        
        image_vitrine.paste(buscape_logo, ( (image_size[0] - 120)/2, 20) )
        
        draw = ImageDraw.Draw(image_vitrine)
        
        title_text = ComposeImage.get_limited_text(title, 18)
        title_font_size = title_font.getsize(title_text)
        
        draw.text(( 120, 90), title_text.decode('utf-8'), font=title_font, fill="black")
        
        label_text = "A partir de"
        label_font_size = label_font.getsize(label_text)
        draw.text(( 120 , 90 + title_font_size[1] + 10), label_text, font=label_font, fill="black")

        price_text = "R$ %s" % (price[0]).replace(".",",")
        price_font_size = price_font.getsize(price_text)
        draw.text(( 120 , 90 + title_font_size[1] + label_font_size[1] + 20), price_text, font=price_font, fill="red")
        
        del draw 
        
        if os.path.exists(image_file_name):
            os.remove(image_file_name)
        
        image_vitrine.paste(image_produto, ( 10, 90 ))
        
        image_vitrine.save(image_file_name,"JPEG", quality=100)
        
        return image_name