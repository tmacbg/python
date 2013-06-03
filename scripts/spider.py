from scrapy.spider import BaseSpider
     
class PaulSmithSpider(BaseSpider):
  domain_name = "paulsmith.co.uk"
  start_urls = ["http://www.paulsmith.co.uk/paul-smith-jeans-253/category.html"]
  
  def parse(self, response):
    open('paulsmith.html', 'wb').write(response.body)
    SPIDER = PaulSmithSpider()

SPIDER = PaulSmithSpider()
