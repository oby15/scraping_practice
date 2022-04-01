import scrapy

# Scrapy tutorial examples

# First example spider, setting out full definitions including start_requests and url in urls, 
# which are included in class otherwise so can be ommited if we want default. Saves entire html to file
# no parsing done yet 

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

# Spider which omits those bit in example one which are defaulted in class, returns dictionaries of data
# extracted from page, finds and proceeds to next page, and scrapes again

class Quotes2Spider(scrapy.Spider):
    
    name = "quotes2"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # See https://docs.scrapy.org/en/latest/intro/tutorial.html for multiple shorter, more 
        # efficient definitions
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    
    import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }



# First attempt at building my own spiders

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