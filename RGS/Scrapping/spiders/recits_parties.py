import scrapy

class QuotesSpider(scrapy.Spider):
    name = "recits_parties"
    start_urls = [
        'http://forum.reseau-js.com/forum/96-vos-r%C3%A9cits-de-parties/'
    ]

    def parse(self, response):
        if len(response.xpath('.//ol')) < 2:
            return
        for aar in response.xpath('.//ol')[1].xpath('.//li'):
            if len(aar.xpath('.//ul')) < 2:
                continue
            stats = aar.xpath('.//ul[@class="ipsDataItem_stats"]').xpath('.//li')
            if len(stats) < 2:
                continue
            yield {
               'title' : aar.xpath('.//a//@title').extract_first(),
    				'replies' : stats[0].xpath('.//span//text()').extract_first(),
    				'views' : stats[1].xpath('.//span//text()').extract_first()
                }

        next_page_list = response.xpath('//li[@class="ipsPagination_next"]')
        if next_page_list is not None:
            next_page = next_page_list.xpath('.//a').extract_first()
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)