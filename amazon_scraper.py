#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
import requests
import time
import datetime


usr = 'API USER'
pas = 'API PWD'
PRC = 151.88


#--------------------------------------------------------------

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8 ,application/signed-exchange;v=b3;q=0.9"
accept_en = "gzip, deflate, br"
accept_lan = "en-US,en;q=0.9"
cache_con = "max-age=0"
cokies = ""
down_link = "0.35"
headers = {'accept': accept,
           'accept-encoding': accept_en,
           'accept-language': accept_lan,
           'cache-control': cache_con,
           'cache': cokies,
           'user-agent': user_agent,}

class AmazonProduct:
    def __init__(self, asin):
        self.asin = asin
        self.page_url = "https://www.amazon.fr/dp/" + self.asin
        self.session = requests.session()
        self.product_price = 0

    def scrape_product_details(self):
        global PRC
        content = self.session.get(self.page_url, headers=headers)
        soup = bs(content.text, "html.parser")
        product_name = soup.select("#productTitle")[0].text
        for _ in product_name:
            if (_ != '\n'):
                print(_, end='')
        self.product_price = float(soup.select("#price_inside_buybox")[0].text[1:-3].replace(',','.'))
        if (self.product_price != PRC):
            msg  = product_name + '\nChanged price from ' + str(PRC) + ' to ' + str(self.product_price) + '€!!!!!!'
            try:
                response = self.session.post('https://smsapi.free-mobile.fr/sendmsg?user='+usr+'&pass='+pas+'&msg='+msg)
                if (response.status_code == 200):
                    PRC = self.product_price
                else:
                    print("\n   SAD RESPONSE  ", response.status_code)
            except:
                print("\n   POST REQUEST FAILED   ")
                return (None)
            print('\n', msg, sep='')
        else:
            print('\nNot ideal price ', self.product_price, '€', sep='')
        return (self.product_price)

product_asin = "B097RJSVGX/ref=twister_B099PGR9T2"
x = AmazonProduct(product_asin)
x.scrape_product_details()
time.sleep(60 * (60 - datetime.datetime.now().minute))
while 1:
    if (x.scrape_product_details() is not None):
        time.sleep(60 * 60)
    else:
        time.sleep(10)
        x.scrape_product_details()
        time.sleep(60 * (60 - datetime.datetime.now().minute))
