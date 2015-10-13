import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "degreeplanner.settings") #Changed in DDS v.0.3

BOT_NAME = 'planner'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'planner.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

#Scrapy 0.20+
ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'planner.scraper.pipelines.DjangoWriterPipeline': 800,
}

#Scrapy up to 0.18
ITEM_PIPELINES = [
                  'dynamic_scraper.pipelines.ValidationPipeline',
                  'planner.scraper.pipelines.DjangoWriterPipeline',
                  ]