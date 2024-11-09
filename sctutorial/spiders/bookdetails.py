import scrapy
import csv
import time
from urllib.parse import urljoin


class BookDetailsSpider(scrapy.Spider):
    name = "BookDetails"

    # Method to get the list of URLs from the CSV file
    def start_requests(self):
        with open('output_books_cleaned.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header if present
            for row in reader:
                # Assuming the Goodreads URL is in the second column (index 1)
                list_url = row[0]
                print(list_url,"::::::::::::::::;;;;;;;;;;;;;;;;;;")
                time.sleep(1)  # Adding delay to prevent hitting the site too fast
                yield scrapy.Request(url=list_url, callback=self.parse)
                

    # Method to parse the individual book page
    def parse(self, response):
        # Extracting data from the Goodreads book page
        # book_name = response.xpath("//h1[@class='gr-h1 gr-h1--serif']/text()").get().strip()
        book_title = response.xpath("//h1[@class='Text Text__title1']/text()").get().strip()
        author = response.xpath("//a/span[@class='ContributorLink__name']/text()").get()
        ratings = response.xpath("//div[@class='RatingStatistics__column']/div[@class='RatingStatistics__meta']/span[1]/text()").get()
        avg_rating = response.xpath("//div[@class='RatingStatistics__rating']/text()").get()
        book_image = response.xpath("//img[@class='ResponsiveImage']/@src").get()

        # Clean up the data, if necessary (e.g., remove extra spaces)
        # book_name = book_name.strip() if book_name else ""
        book_title = book_title.strip() if book_title else ""
        author = author.strip() if author else ""
        ratings = ratings.strip() if ratings else ""
        avg_rating = avg_rating.strip() if avg_rating else ""
        book_image = book_image.strip() if book_image else ""

        # Yielding the extracted data to be saved in the CSV
        yield {
            # 'book_name': book_name,
            'book_title': book_title,
            'author': author,
            'ratings': ratings,
            'avg_rating': avg_rating,
            'book_image': book_image,
            'book_url': response.url  # Include the URL of the book page
        }

        # Handle pagination if there is any (for the list page, not for the book page)
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        if next_page:
            # Construct the full URL for the next page
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # Setting up the output format for saving the scraped data in a CSV file
    custom_settings = {
        'FEEDS': {
            'book_details.csv': {
                'format': 'csv',
                'fields': ['book_title', 'author', 'ratings', 'avg_rating', 'book_image', 'book_url'],
                'overwrite': True,  # Overwrite the file if it exists
            },
        },
    }
