import scrapy
from books.items import BooksItem


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            yield item

        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            # concatenate the next page's url to the website base domain
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Navigating to the next page with URL {next_page_url}.")
            # yields a scrapy.Request object, passing it the URL.
            # makes a recursive request to the next using the .parse() method
            yield scrapy.Request(url=next_page_url, callback=self.parse)
