import scrapy
import datetime


class ParadoxAARSpider(scrapy.Spider):
    name = "paradox_aar"
    start_urls = [
        'https://forum.paradoxplaza.com/forum/index.php?forums/euiv-after-action-reports-aar.816/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/crusader-kings-ii-after-action-reports-aar.684/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/stellaris-after-action-reports-aar.944/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/hearts-of-iron-4-after-action-reports-aar.947/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/victoria-2-after-action-reports-aar.548/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/hoi3-after-action-reports-aar.435/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/darkest-hour-after-action-reports-aar.606/',
        'https://forum.paradoxplaza.com/forum/index.php?forums/eu3-after-action-reports-aar.360/'
    ]

    def get_game(self, response):
        url = response.url
        if 'euiv' in url:
            return 'EUIV'
        if 'crusader-kings-ii' in url:
            return 'CK2'
        if 'stellaris' in url:
            return 'Stellaris'
        if 'hearts-of-iron-4' in url:
            return 'HoI4'
        if 'victoria-2' in url:
            return 'Victoria 2'
        if 'hoi3' in url:
            return 'HoI3'
        if 'darkest-hour' in url:
            return 'DarkestHour'
        if 'eu3' in url:
            return 'EU3'


    def parse(self, response):
        today = datetime.date.today()
        base_url = 'https://forum.paradoxplaza.com/forum/'
        game = self.get_game(response)
        for aar in response.xpath('.//ol')[-1].xpath('.//li'):
            stat_div = aar.xpath('.//div[@class="listBlock stats pairsJustified"]//dd//text()')
            if len(stat_div) < 2:
                continue
            yield {
                'title': aar.xpath('.//h3[@class="title"]//a//text()').extract_first(),
                'url': base_url + aar.xpath('.//h3[@class="title"]//a//@href').extract_first(),
                'replies': stat_div[0].extract().replace('\n', ''),
                'views': stat_div[1].extract().replace('\n', ''),
                'date': today,
                'game': game
            }

        last_nav_link = response.xpath('.//div[@class="PageNav"]')[0].xpath('.//a')[-1]
        if last_nav_link.xpath('.//text()').extract()[0] == 'Next >':
            next_page = last_nav_link.xpath('.//@href').extract()[0]
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
