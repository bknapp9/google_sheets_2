from selenium import webdriver
from parsel import Selector
from time import sleep
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(options=options)


driver.get("https://www.boldpreciousmetals.com/product/3260/2022-american-gold-eagle-1-oz-bu?fromPage=AdvSrch-PrdLst&fromUrl=%5Bobject%20Object%5D")
sleep(2)
coin_name = driver.find_element(By.XPATH, "//h1").text
coin_price = driver.find_element(By.XPATH, "//span[@class='woocommerce-Price-amount amount']").text
print(coin_name)