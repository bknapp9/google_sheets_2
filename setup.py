# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'gold_coins_spider',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        'gold_coins_spider': ['resources/*.pickle']
    },
    entry_points = {'scrapy': ['settings = gold_coins_spider.settings']},
)
