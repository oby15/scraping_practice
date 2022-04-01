import scrapy


class ProductSpider(scrapy.Spider):
    
    name = "product"
    start_urls = [
        'https://rethread.uk/collections/new-arrivals',
    ]

    # 1. Watch out to not assing variable with get() as that assigns string, was response object, not string
    # 2. XX Issue, at the moment only seem to be able to drill down through selectors to prices iteratively,
    # rather than achieve with single response.css argument...seems to just return empty
    def parse(self, response):
        products = response.css('div.price__regular')
        products2 = products.css('dd')
        prices = products2.css('span') 
        for product in prices:
            yield {
                'price': product.css('span::text').getall(),
            }

        # See https://docs.scrapy.org/en/latest/intro/tutorial.html for multiple shorter, more 
        # efficient definitions
        #next_page = response.css('li.next a::attr(href)').get()
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)   