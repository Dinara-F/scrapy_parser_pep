import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        numerical_index = response.css('section[id=numerical-index]')
        all_peps = numerical_index.css('a[href^="/pep-"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        number = int(title.split()[1])
        name = ' '.join(title.split()[3:])
        status = response.css('dt:contains("Status") + dd::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status
        }
        yield PepParseItem(data)
