import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css('a[href^="/pep-"]')

        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        table = response.css('dl.rfc2822')
        number = title.split()[1]
        name = ' '.join(title.split()[3::1])
        status = table.css('dt:contains("Status") + dd::text').get()

        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
