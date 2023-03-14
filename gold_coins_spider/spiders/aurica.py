from scrapy import Spider
from time import sleep
import pytz
from datetime import datetime


class aurica(Spider):
    name = 'aurica'
    allowed_domains = ['aurica.cl', 'compreoro.com', 'gainesvillecoins.com', 'boldpreciousmetals.com', 'hardassetsalliance.com']
    start_urls = ['https://aurica.cl/tienda/gold-maple-leaf-1oz/',
                  'https://aurica.cl/tienda/gold-canadian-maple-leaf-1-2-oz/',
                  'https://aurica.cl/tienda/american-eagle-1-2-oz/',
                  'https://aurica.cl/tienda/moneda-de-oro-maple-leaf-canada-1-4-oz/',
                  'https://aurica.cl/tienda/gold-maple-leaf-1-10oz/',
                  'https://aurica.cl/tienda/moneda-de-oro-american-eagle-1-oz/',
                  'https://compreoro.com/producto/moneda-canadian-maple-leaf-gold-1-oz/',
                  'https://compreoro.com/producto/moneda-american-eagle-type-2-gold-1-oz/',
                  'https://compreoro.com/producto/moneda-canadian-maple-leaf-gold-1-oz-cev/',
                  'https://compreoro.com/producto/moneda-american-eagle-type-2-gold-1-oz-cev/',
                  'https://online.kitco.com/buy/3110/1-oz-Gold-Canadian-Maple-Leaf-Coin-9999-3110',
                  'https://online.kitco.com/buy/3100/1-2-oz-Gold-Canadian-Maple-Leaf-Coin-9999-3100',
                  'https://online.kitco.com/buy/3101/1-4-oz-Gold-Canadian-Maple-Leaf-Coin-9999-3101',
                  'https://online.kitco.com/buy/3102Y2023/2023-1-10-oz-Gold-Canadian-Maple-Leaf-Coin-9999-BU-3102Y2023',
                  'https://online.kitco.com/buy/3000/1-oz-Gold-American-Eagle-Coin-9167-3000',
                  'https://online.kitco.com/buy/3001/1-2-oz-Gold-American-Eagle-Coin-9167-3001'
                  'https://orionmetalexchange.com/product/gold-american-eagle-1-4-oz/',
                  'https://orionmetalexchange.com/product/gold-american-eagle-1-10-oz/',
                  ]

    def parse(self, response):
        time = datetime.now(pytz.timezone('Chile/Continental')).strftime("%Y:%m:%d %H:%M:%S")
        url = response.url
        # aurica
        if "aurica.cl" in response.url:
            coin_name = response.css("h1::text").get()
            coin_price = response.xpath("//*[@class='price']/span/bdi/text()").get()
            if coin_price:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": time,
                       "coin_price": coin_price}
            else:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": time,
                       "coin_price": "Sin stock"}

        # compreoro
        elif "compreoro.com" in response.url:
            coin_name = response.xpath("//h1/text()").extract_first()
            if "cev" in response.url:
                coin_price = response.xpath("//*[@class='price product-page-price ']/span/bdi/text()").extract_first()
            else:
                coin_price = response.xpath("//*[@class='woocommerce-Price-amount amount']/bdi/text()")[1].extract()
            if coin_price:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": time,
                       "coin_price": coin_price}
            else:
                yield {"url": url,
                       "coin_name": coin_name,
                       "time": time,
                       "coin_price": "Sin stock"}
        # kitco
        elif "online.kitco.com" in response.url:
            coin_name = response.xpath("//h1/span/text()").extract_first()
            table = response.xpath("//table[contains(@class, 'bulk_discount_list')]")[0]
            trs = table.xpath(".//tr")[1:]
            for tr in trs:
                coin_price = tr.xpath("//td/text()")[1].extract().strip()
                coin_price = coin_price.replace("$", "")
            if coin_price:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": time,
                    "coin_price": coin_price
                }
            else:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": time,
                    "coin_price": "Sin stock"
            }
        elif "orionmetalexchange.com" in response.url:
            coin_name = response.xpath("//h1/text()").extract_first()
            coin_price = response.xpath("//*[@class='woocommerce-Price-amount amount']/bdi/text()").extract_first()
            if coin_price:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": time,
                    "coin_price": coin_price
                }
            else:
                yield {
                    "url": url,
                    "coin_name": coin_name,
                    "time": time,
                    "coin_price": "Sin stock"
                }
