# -*- coding: utf-8 -*-
import scrapy

class SpidrItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    avgPrice = scrapy.Field()
    features = scrapy.Field()


class spidrSpider(scrapy.Spider):
    name = "spidr"
    allowed_domains = ["hotline.ua"]

    # lets try to use generator expression here instead of list
    start_urls = ["http://hotline.ua/mobile/mobilnye-telefony-i-smartfony/"]
    #start_urls = ( ("http://hotline.ua/mobile/mobilnye-telefony-i-smartfony/?p=" + str(n)) for n in range(88) )


    def parse(self, response):
        for url in response.xpath("//div[@class='ttle']/a/@href").extract():
            url = "http://hotline.ua" + url
            #print url
            #raw_input("Press something pls")
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        item = SpidrItem()

        item['name'] = response.xpath("//head/meta[@property='og:title']/@content").extract()[0]
        item['brand'] = response.xpath("//table[@id='full-props-list']//a[@class='g_statistic' and @data-statistic-key='stat36']/text()").extract()[0]
        

        price = response.xpath("//script[contains(text(), 'averagePrice')]").extract()[0]
        price = price[price.index('Price'):price.index('Price')+20]
        price = price[price.index(':')+2:price.index(',')]
        item['avgPrice'] = price


        raw_features_names,raw_features_contents = response.xpath("//table[@id='full-props-list']/tr/th/span/text()").extract(), response.xpath("//table[@id='full-props-list']/tr/td/span").extract()


        features_names = []
        for itm in raw_features_names:
            if len (itm.strip()) >= 3:
                features_names.append(itm.strip())

        features_contents = []
        for itm in raw_features_contents:
            features_contents.append( (itm[6:-7]) )

        if len(features_names) == len(features_contents):
            dictionary = {}
            for i in range(len(features_names)):
                dictionary[features_names[i]] = features_contents[i]

        # manufacturer == brand, right? :) if it exists
        if u'Производитель' in dictionary.keys():
            dictionary[u'Производитель'] = item['brand']

        # model on manufacturer's site (if exists)
        if u'Модель из линейки' in dictionary.keys():
            if 'href' in dictionary[u'Модель из линейки']:
                tempstr = dictionary[u'Модель из линейки'][10:-4]
                tempstr = u"http://hotline.ua/" + tempstr[:tempstr.index("\"")]
                dictionary[u'Модель из линейки'] = tempstr

        # same for product link
        if u'Товар на сайте производителя' in dictionary.keys():
            if 'href' in dictionary[u'Товар на сайте производителя']:
                tempstr = dictionary[u'Товар на сайте производителя'][9:-9]
                tempstr = tempstr[:tempstr.index("\"")]
                dictionary[u'Товар на сайте производителя'] = tempstr

        item['features'] = dictionary

        yield item