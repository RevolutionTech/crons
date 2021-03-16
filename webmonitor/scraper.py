import re
import time

import requests


class PaginatedWebScraper:

    PAGE_QUERY_PARAM_NAME = "page"

    def __init__(self, url, regex):
        self.url = url
        self.regex = re.compile(regex, re.IGNORECASE)

    def find_url_containing_regex(self):
        """
        Paginates through a webpage until a regex matches.
        If the regex is eventually found, returns the URL containing the match.
        If all pages have been searched, returns False.
        """
        seen_webpages = set()
        page = 1

        while True:
            response = requests.get(self.url, {self.PAGE_QUERY_PARAM_NAME: page})
            if self.regex.search(response.content.decode("utf-8")):
                return response.request.url

            # Stop once we see a page that we've seen before.
            # That means we've cycled through all of the available pages
            # without finding anything.
            if response.content in seen_webpages:
                return False

            seen_webpages.add(response.content)
            page += 1

            # A very primitive form of rate-limiting.
            # Avoid overwhelming the server with too many requests.
            time.sleep(2)
