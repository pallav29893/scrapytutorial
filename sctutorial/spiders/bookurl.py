import scrapy
import csv
from urllib.parse import urljoin
import time 

class BooksSpider(scrapy.Spider):
    name = "book"

    def start_requests(self):

        # Open the CSV file containing the list URLs
        with open('goodreads_lists.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header if there is one
            for row in reader:
                # Assuming the URL is in the first column
                list_url = row[1]

        #         # Ensure that list_url is a full URL
        #         if not list_url.startswith('http'):
        #             list_url = urljoin(base_url, list_url)
        #             print(list_url,'<<<<<<<<<<<<<<>>>>>>>>>>>>>>')

        #         # Initiate the request to the list URL
                time.sleep(2)
                yield scrapy.Request(url=list_url, callback=self.parse)

    def parse(self, response):
        # print(response.xpath("//table//tr").get(),'fsdfdsdfsgggggggggggggggggggggggg')
        # seen_urls = set()  # Initialize a set to track seen book URLs
        for items in response.xpath("//table//tr"):
            book_url =  "https://www.goodreads.com" + items.xpath(".//td[3]/a/@href").get()
            print(book_url, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


        # for items in response.xpath("//table//tr"):
        #     book_url = "https://www.goodreads.com" + items.xpath(".//td[3]/a/@href").get()
        #     if book_url and book_url not in seen_urls:  # Check for duplicates
        #         seen_urls.add(book_url)  # Add to seen URLs
        #         print(book_url, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


       
        # Loop through each list title and link and yield as a dictionary
        # for link in zip():
            yield {
                # 'list_name': title.strip(),
                'list_link': book_url
            }

        # Handle pagination to scrape the next page of the same list if it exists
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        if next_page:
            # Construct the full URL for the next page
            next_page_url = urljoin("https://www.goodreads.com", next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # Set the output format to CSV for all the extracted data
    custom_settings = {
        'FEEDS': {
            'output_books.csv': {
                'format': 'csv',
                'fields': ['list_link'],  # Fields to export
                'overwrite': True,  # Overwrite the file if it exists
            },
        },
    }


# import scrapy
# import csv
# import time
# from urllib.parse import urljoin
# import os

# class BooksSpider(scrapy.Spider):
#     name = "book"

#     def start_requests(self):
#         # Initialize a set to track existing book URLs
#         self.existing_urls = set()

#         # Check if the output CSV exists and read existing URLs
#         if os.path.exists('output_books.csv'):
#             with open('output_books.csv', 'r') as file:
#                 reader = csv.DictReader(file)
#                 for row in reader:
#                     self.existing_urls.add(row['list_link'])

#         # Open the CSV file containing the list URLs
#         with open('goodreads_lists.csv', 'r') as file:
#             reader = csv.reader(file)
#             next(reader)  # Skip the header if there is one
#             for row in reader:
#                 list_url = row[1]
#                 time.sleep(2)
#                 yield scrapy.Request(url=list_url, callback=self.parse)

#     def parse(self, response):
#         for items in response.xpath("//table//tr"):
#             book_url = "https://www.goodreads.com" + items.xpath(".//td[3]/a/@href").get()
#             if book_url and book_url not in self.existing_urls:  # Check for duplicates
#                 self.existing_urls.add(book_url)  # Add to seen URLs
#                 print(book_url, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#                 # Yield only unique book URLs
#                 yield {
#                     'list_link': book_url
#                 }

#         # Handle pagination to scrape the next page of the same list if it exists
#         next_page = response.xpath("//a[@class='next_page']/@href").get()
#         if next_page:
#             next_page_url = urljoin("https://www.goodreads.com", next_page)
#             yield scrapy.Request(next_page_url, callback=self.parse)

#     # Set the output format to CSV for all the extracted data
#     custom_settings = {
#         'FEEDS': {
#             'output_books.csv': {
#                 'format': 'csv',
#                 'fields': ['list_link'],  # Fields to export
#                 'overwrite': False,  # Do not overwrite; append data
#             },
#         },
#     }

# import numpy as np
# import csv

# # Step 1: Load the CSV data into a NumPy array
# # Assuming you have a CSV file 'output_books.csv'
# data = np.genfromtxt('output_books.csv', delimiter=',', dtype=None, encoding=None, names=True)

# # Step 2: Remove duplicates by using np.unique with the 'axis' argument
# # The 'axis=0' argument ensures that rows are compared for uniqueness
# # 'return_index' helps us keep the first occurrence of each row

# unique_data = np.unique(data, axis=0)

# # Step 3: Save the cleaned (unique) data back to a new CSV file
# # We use 'np.savetxt' to write the data to a CSV file

# # Write header and data to a new CSV
# header = data.dtype.names  # Get column names from the dtype
# np.savetxt('output_books_cleaned.csv', unique_data, delimiter=',', fmt='%s', header=','.join(header), comments='')

# print("Duplicates removed and saved to output_books_cleaned.csv")
