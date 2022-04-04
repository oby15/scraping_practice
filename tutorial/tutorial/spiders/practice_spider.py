import scrapy

# XX Version with response.follow not working - think it might be because relative path of next pages
# are not defined with / (instead e.g ?page=2)
class ProductSpider(scrapy.Spider):
    
    name = "product"
    start_urls = [
        'https://rethread.uk/collections/new-arrivals',
    ]

    # 1. Watch out to not assing variable with get() as that assigns string, was response object, not string
    # 2. XX at the moment only seem to be able to drill down through selectors to prices iteratively,
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
        # For CSS selector class names with spaces, replace with dot notation!
        temp = response.css('a.btn.btn--tertiary.btn--narrow::attr(href)').get()
        next_page_rel = temp[temp.index("?"):]
        if next_page_rel is not None:
            yield response.follow(next_page_rel, callback=self.parse)


# Partially working version using scrapy.Request to spider consecutive pages - building absolute url,
# however, doesn't follow all consecutive page links, as fails to differentiate between next and
# proceeding page links (as have same css selector) once it lands on page 2, so goes back to pg 1 again
# and finishes. 
class ProductSpider2(scrapy.Spider):
    
    name = "product2"
    start_urls = [
        'https://rethread.uk/collections/new-arrivals',
    ]

    def parse(self, response):
        products = response.css('div.price__regular')
        products2 = products.css('dd')
        prices = products2.css('span') 
        for product in prices:
            yield {
                'price': product.css('span::text').getall(),
            }
        temp = response.css('a.btn.btn--tertiary.btn--narrow::attr(href)').get()
        next_page_rel = temp[temp.index("?"):]
        if next_page_rel is not None:
            next_page = response.urljoin(next_page_rel)
            yield scrapy.Request(next_page, callback=self.parse)


# Version to crawl all product pages using xpath selector to isole finding next page link
class ProductSpider3(scrapy.Spider):
    
    name = "product3"
    start_urls = [
        'https://rethread.uk/collections/new-arrivals',
    ]

    def parse(self, response):
        products = response.css('div.price__regular')
        products2 = products.css('dd')
        prices = products2.css('span') 
        for product in prices:
            yield {
                'price': product.css('span::text').getall(),
            }
        # Finds unique text in child element and then uses .. notation to select parent element,
        # and then selecting the href of that element
        temp = response.xpath('//span[contains(text(), "Next page")]/../@href').get()
        next_page_rel = temp[temp.index("?"):]
        if next_page_rel is not None:
            next_page = response.urljoin(next_page_rel)
            yield scrapy.Request(next_page, callback=self.parse)

# Version to get product title and price for all products on site.
class ProductSpider4(scrapy.Spider):
    
    name = "product4"
    start_urls = [
        'https://rethread.uk/collections/new-arrivals',
    ]

    def parse(self, response):
        products = response.css('div.grid-view-item.product-card')
        for product in products:
            yield {
                'title': product.css('div.h4.grid-view-item__title.product-card__title::text').getall(),
                'price': product.css('span.price-item.price-item--regular::text').getall(),
            }
        # Finds unique text in child element and then uses .. notation to select parent element,
        # and then selecting the href of that element
        temp = response.xpath('//span[contains(text(), "Next page")]/../@href').get()
        next_page_rel = temp[temp.index("?"):]
        if next_page_rel is not None:
            next_page = response.urljoin(next_page_rel)
            yield scrapy.Request(next_page, callback=self.parse)