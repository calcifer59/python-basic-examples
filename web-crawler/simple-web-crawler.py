from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse
from urllib.error import HTTPError
from http.client import InvalidURL
from ssl import _create_unverified_context

class AnchorParser(HTMLParser):
    "Basic HTML parser that gathers a set of all href values in a webpage by targetting the anchor tag"

    def __init__(self, baseURL = ""):
        """Constructor for AnchorParser

        Args:
            baseURL (str): Base URL for the HTML content

        Returns:
            None
        """
        # Parent class constructor
        HTMLParser.__init__(self)
        # Set of all hyperlinks in the web page
        self.pageLinks = set()
        # The base url of the webpage to parse
        self.baseURL = baseURL

    def getLinks(self):
        """Return the set of absolute URLs in the HTML content

        Returns:
            set: Absolute URLs found in HTML content
        """
        return self.pageLinks

    def handle_starttag(self, tag, attrs):
        """Override handle_starttag to target anchor tags

        Returns:
            None
        """
        # Identify anchor tags
        if tag == "a":
            for(attribute, value) in attrs:
                # Anchor tags may have more than 1 attribute, but handle_starttag will only target href
                # Attribute examples: href, target, rel, etc
                # Attribute list can be found at: https://www.w3schools.com/tags/tag_a.asp
                if attribute == "href":
                    # Form an absolute URL based on the relative URL
                    absoluteUrl = urljoin(self.baseURL, value)
                    # We want to avoid href values that are not http/https
                    # Example: <a href="mailto:person@some.com">Send Email Now!</a>
                    if urlparse(absoluteUrl).scheme in ["http", "https"]:
                        # Once a new hyperlink is obtained, add it to the set
                        self.pageLinks.add(absoluteUrl)


class MyWebCrawler(object):
    "Basic Web Crawler using only Python Standard Libraries"

    def __init__(self, url, maxCrawl=10):
        """Constructor for MyWebCrawler

        Args:
            url (str): The starting URL for the web crawler
            maxCrawl (int): Max amount of URLs to crawl

        Returns:
            None
        """
        self.visited = set() # To track all visited urls
        self.starterUrl = url
        self.max = maxCrawl

    def crawl(self):
        """Tracks URLs visited in a set in order to crawl through different sites
        Will only crawl through as many URLs as declared with 'maxCrawl' when instantiating MyWebCrawler

        Returns:
            None
        """
        urlsToParse = {self.starterUrl}
        # While there are still more URLs to parse and we have not exceeded the crawl limit
        while(len(urlsToParse) > 0 and len(self.visited) < self.max):
            # Get the next URL to visit and remove it the set
            nextUrl = urlsToParse.pop()
            # Skip the next URL if it has already been visited
            if nextUrl not in self.visited:
                # Mark the next URL as visited
                self.visited.add(nextUrl)
                # Call the .parse method to make a web request
                # and parse any new URLs from the HTML content
                # any new URLs found will be appended to the urlsToParse set
                print("Parsing: {}".format(nextUrl))
                urlsToParse |= self.parse(nextUrl)

    def parse(self, url):
        """Makes a web request and uses an AnchorParser object to parse the HTML content

        Args:
            url (str): URL to request and parse

        Returns:
            set: Absolute URLs found in HTML content

        Exceptions Caught:
            HTTPError, InvalidURL, UnicodeDecodeError
        """
        try:
            # Open the URL, read content, decode content
            htmlContent = urlopen(url, context=_create_unverified_context()).read().decode()
            # Initiate the AnchorParser object
            parser = AnchorParser(url)
            # Feed in the HTML content to our AnchorParser object
            parser.feed(htmlContent)
            # The AnchorParser object has a set of absolute URLs that can be returned
            return parser.getLinks()
        except (HTTPError, InvalidURL, UnicodeDecodeError):
            # In the case we get any http error
            # Example: 403 code
            print("FAILED: {}".format(url))
            return set()

    def getVisited(self):
        """Returns the set of URLs visited
        Note: Will include urls that raised HTTPError and InvalidURL

        Returns:
            set: All URLs visited/parsed
        """
        return self.visited


if __name__ == "__main__":
    # Change the URL below
    crawler = MyWebCrawler("https://CHANGEME.com", maxCrawl=20)
    crawler.crawl()
    print("\nThe following sites were visited:\n{}".format(crawler.getVisited()))
