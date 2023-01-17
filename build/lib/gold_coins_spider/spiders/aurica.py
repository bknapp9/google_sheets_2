from scrapy import Spider
from time import time, ctime, sleep
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from parsel import Selector

class aurica(Spider):
    name = 'aurica'
    allowed_domains = ['aurica.cl', 'compreoro.com', 'gainesvillecoins.com', 'boldpreciousmetals.com', 'hardassetsalliance.com']
    start_urls = ['https://aurica.cl/tienda/gold-maple-leaf-1oz/',
                  'https://aurica.cl/tienda/gold-canadian-maple-leaf-1-2-oz/',
                  'https://aurica.cl/tienda/american-eagle-1-2-oz/',
                  'https://aurica.cl/tienda/moneda-de-oro-maple-leaf-canada-1-4-oz/',
                  'https://aurica.cl/tienda/gold-maple-leaf-1-10oz/',
                  'https://compreoro.com/producto/moneda-canadian-maple-leaf-gold-1-oz/',
                  'https://compreoro.com/producto/moneda-american-eagle-type-2-gold-1-oz/',
                  'https://compreoro.com/producto/moneda-canadian-maple-leaf-gold-1-oz-cev/',
                  'https://compreoro.com/producto/moneda-american-eagle-type-2-gold-1-oz-cev/',
                  'https://www.gainesvillecoins.com/products/158985/1-oz-american-gold-eagle-coins',
                  'https://www.gainesvillecoins.com/products/158550/1-2-oz-american-gold-eagle-coins',
                  'https://www.gainesvillecoins.com/products/180330/2021-1-4-oz-gold-american-eagle-brilliant-uncirculated',
                  'https://www.gainesvillecoins.com/products/180331/2021-1-10-oz-gold-american-eagle-brilliant-uncirculated',
                  'https://hardassetsalliance.com/gold-coins/american-gold-eagles-1-oz/',
                  'https://hardassetsalliance.com/gold-coins/american-eagle-50-oz/',
                  'https://www.boldpreciousmetals.com/product/3260/2022-american-gold-eagle-1-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D',
                  'https://www.boldpreciousmetals.com/product/3264/2022-american-gold-eagle-1-2-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D',
                  'https://www.boldpreciousmetals.com/product/3263/2022-american-gold-eagle-1-4-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D',
                  'https://www.boldpreciousmetals.com/product/3262/2022-american-gold-eagle-1-10-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D',
                  'https://orionmetalexchange.com/product/gold-american-eagle-1-4-oz/',
                  'https://orionmetalexchange.com/product/gold-american-eagle-1-10-oz/',
                  ]

    prices_au = []
    prices_co = []
    prices_de = []

    def parse(self, response):
        t = time()
        url = response.url
        # aurica
        if "aurica.cl" in response.url:
            coin_name = response.css("h1::text").get()
            coin_price = response.xpath("//*[@class='price']/span/bdi/text()").get()
            if coin_price:
                n = coin_price.replace(".", "")
                aurica.prices_au.append(n)
                if len(aurica.prices_au) == 5:
                    aurica.prices_au = list(map(int, aurica.prices_au))
                    aurica.prices_au.sort(reverse=True)
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": ctime(t),
                       "coin_price": coin_price}
            else:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": ctime(t),
                       "coin_price": "Sin stock"}

        # compreoro
        elif "compreoro.com" in response.url:
            coin_name = response.xpath("//h1/text()").extract_first()
            if "cev" in response.url:
                coin_price = response.xpath("//*[@class='price product-page-price ']/span/bdi/text()").extract_first()
            else:
                coin_price = response.xpath("//*[@class='price product-page-price price-not-in-stock']/span/bdi/text()").extract_first()
            if coin_price:
                n = coin_price.replace(".", "")
                aurica.prices_co.append(n)
                if len(aurica.prices_co) >= 3:
                    aurica.prices_co = list(map(int, aurica.prices_co))
                    aurica.prices_co.sort(reverse=True)
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": ctime(t),
                       "coin_price": coin_price}
            else:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": ctime(t),
                       "coin_price": "Sin stock"}
        # Gainesville
        elif "gainesvillecoins.com" in response.url:
            coin_name = response.xpath("//h1/text()").extract_first()
            coin_price = response.xpath("//td[2]/text()").extract_first()
            if coin_price:
                coin_price = coin_price.replace("$", "")
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": ctime(t),
                       "coin_price": coin_price}
            else:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": ctime(t),
                       "coin_price": "Sin stock"}

        # hardassetsalliance
        elif "hardassetsalliance.com" in response.url:
            coin_name = response.xpath("//h1/text()").extract_first().strip()
            coin_price = response.xpath("//span[@itemprop='price']/text()").extract_first().replace("\n", "").strip()
            if coin_price:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": ctime(t),
                    "coin_price": coin_price
                }
            else:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": ctime(t),
                    "coin_price": "Sin stock"
            }
        elif "orionmetalexchange.com" in response.url:
            coin_name = response.xpath("//h1/text()").extract_first()
            coin_price = response.xpath("//*[@class='woocommerce-Price-amount amount']/bdi/text()").extract_first()
            if coin_price:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": ctime(t),
                    "coin_price": coin_price
                }
            else:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": ctime(t),
                    "coin_price": "Sin stock"
                }

        # boldpreciousmetals
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            driver = webdriver.Chrome(options=options)
            if "1-oz" in response.url:
                driver.get("https://www.boldpreciousmetals.com/product/3260/2022-american-gold-eagle-1-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D")
                sleep(2)
            elif "1-2-oz" in response.url:
                driver.get("https://www.boldpreciousmetals.com/product/3264/2022-american-gold-eagle-1-2-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D")
                sleep(2)
            elif "1-4-oz" in response.url:
                driver.get("https://www.boldpreciousmetals.com/product/3263/2022-american-gold-eagle-1-4-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D")
                sleep(2)
            elif "1-10-oz" in response.url:
                driver.get("https://www.boldpreciousmetals.com/product/3262/2022-american-gold-eagle-1-10-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D")
                sleep(2)

            coin_name = driver.find_element(By.XPATH, "//h1").text
            coin_price = driver.find_element(By.XPATH, "//span[@class='woocommerce-Price-amount amount']").text

            if coin_price:
                coin_price = coin_price.replace("$", "")
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": ctime(t),
                    "coin_price": coin_price
                }
            else:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": ctime(t),
                    "coin_price": "Sin stock"
                }
"""
process = CrawlerProcess()
process.crawl(aurica)
process.start()
"""
