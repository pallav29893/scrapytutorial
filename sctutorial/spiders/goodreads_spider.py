import scrapy

# class GoodreadsSpider(scrapy.Spider):
#     name = "goodreads"

#     # Starting URL for the lists page
#     start_urls = ["https://www.goodreads.com/list/popular_lists?page=1&ref=ls_pl_seeall"]

#     def parse(self, response):
#         # print(response.text)
#         # Extracting links for each book list (list titles and links)
#         list_links = response.css("a.listName::attr(href)").getall()
#         list_titles = response.css("a.listName::text").getall()

#         # Loop through each list title and link
#         for title, link in zip(list_titles, list_links):
#             # Yield the list name and its link
#             yield {
#                 'list_name': title.strip(),
#                 'list_link': response.urljoin(link)
#             }

#             # Follow the link to the individual list page for further details (books in that list)
#             yield response.follow(link, self.parse_list)

#         # Handling pagination if there are multiple pages of lists
#         next_page = response.css("li.next a::attr(href)").get()
#         if next_page:
#             yield response.follow(next_page, self.parse)

#     # def parse_list(self, response):
#     #     # Extracting book details from the list page (book titles, authors, and ratings)
#     #     book_titles = response.css("span.bookTitle::text").getall()
#     #     authors = response.css("span.authorName::text").getall()
#     #     ratings = response.css("span.minirating::text").getall()

#     #     # Yield the extracted book details
#     #     for title, author, rating in zip(book_titles, authors, ratings):
#     #         yield {
#     #             'book_title': title.strip(),
#     #             'author': author.strip(),
#     #             'rating': rating.strip(),
#     #             'list_page': response.url  # Keeping track of which list this book came from
#     #         }

#     #     # Handling pagination for the individual list page (if there are more pages of books in this list)
#     #     next_page = response.css("li.next a::attr(href)").get()
#     #     if next_page:
#     #         yield response.follow(next_page, self.parse_list)



# class GoodreadsSpider(scrapy.Spider):
#     name = "goodreads"

#     # Starting URL for the lists page
#     start_urls = ["https://www.goodreads.com/list/popular_lists?page=1&ref=ls_pl_seeall"]

#     def parse(self, response):
#         links = response.xpath("//a[@class='listTitle']/@href").getall()
#         titles = response.xpath("//a[@class='listTitle']/@text").getall()
#         links = ["https://www.goodreads.com" + link for link in links if link]
#         print(links, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         # Extracting links for each book list (list titles and links)
#         list_links = response.css("a.listName::attr(href)").getall()
#         list_titles = response.css("a.listName::text").getall()

#         # Loop through each list title and link
#         for title, link in zip(list_titles, list_links):
#             # Yield the list name and its link
#             yield {
#                 'list_name': title.strip(),
#                 'list_link': response.urljoin(link)
#             }

#         # Handling pagination if there are multiple pages of lists
#         next_page = response.css("li.next a::attr(href)").get()
#         if next_page:
#             yield response.follow(next_page, self.parse)



class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"
    
    # Starting URL for the lists page
    start_urls = ["https://www.goodreads.com/list/popular_lists?page=1&ref=ls_pl_seeall"]

    def parse(self, response):
        # Extracting the list titles and links
        list_links = response.xpath("//a[@class='listTitle']/@href").getall()
        list_titles = response.xpath("//a[@class='listTitle']/text()").getall()

        # Construct the full URLs for the list links
        list_links = ["https://www.goodreads.com" + link for link in list_links if link]

        # Print for debugging to see what has been extracted
        print(list_titles, list_links)

        # Loop through each list title and link and yield as a dictionary
        for title, link in zip(list_titles, list_links):
            yield {
                'list_name': title.strip(),
                'list_link': link
            }
        # Handling pagination if there are multiple pages of lists
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        print(next_page,">>>><<<<<>><<<")
        if next_page:
            # Follow the next page link
            next_page_url =  "https://www.goodreads.com" + next_page
            print(next_page_url,"<<<<<<<<<<<<<<<<<<")
            yield scrapy.Request(next_page_url, callback=self.parse)

# class GoodreadsSpider(scrapy.Spider):
#     name = "goodreads"
#     start_urls = ["https://www.goodreads.com/list/popular_lists?page=1&ref=ls_pl_seeall"]

#     def parse(self, response):
#         # Check if we are successfully getting the page
#         self.log(f"Scraping page: {response.url}")

#         # Extract list titles and links
#         list_links = response.css("a.listName::attr(href)").getall()
#         list_titles = response.css("a.listName::text").getall()

#         # Check if we got any results
#         if not list_links or not list_titles:
#             self.log("No lists found! Check the selectors or page structure.")

#         # Loop through each list title and link
#         for title, link in zip(list_titles, list_links):
#             # Yield the list name and its link
#             yield {
#                 'list_name': title.strip(),
#                 'list_link': response.urljoin(link)
#             }

#         # Handle pagination if there are multiple pages
#         next_page = response.css("li.next a::attr(href)").get()
#         if next_page:
#             self.log(f"Following pagination link: {next_page}")
#             yield response.follow(next_page, self.parse)