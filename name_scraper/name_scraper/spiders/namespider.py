import scrapy


class NamespiderSpider(scrapy.Spider):
    name = "namespider"
    start_urls = ["https://adoption.com/baby-names/origin/Filipino?page=1"]

    def parse(self, response):
        # Extract data from each column
        names    = response.xpath('//table//tr/td[1][@class="text-wrap"]/text()').getall()
        meanings = response.xpath('//table//tr/td[2][@class="text-wrap"]/text()').getall()
        genders  = response.xpath('//table//tr/td[contains(@class, "d-none") and contains(@class, "d-sm-table-cell")]/text()').getall()
        origins  = response.xpath('//table//tr/td[4][@class="text-wrap"]/text()').getall()
        
        max_length = max(len(names), len(meanings), len(genders), len(origins))

        # Yield dictionaries containing data from each column
        for i in range(max_length):
            if i < len(names) and i < len(meanings) and i < len(genders) and i < len(origins): 
                yield {
                    'name': names[i].strip(),
                    'meanings': meanings[i].strip(),
                    'gender': genders[i].strip(),
                    'origin': origins[i].strip(),
            }
        
        next_page = response.xpath('//li[@class="page-item"]/a[@class="page-link"]/@href').extracr()

        if next_page:
            yield response.follow(next_page[-1], callback=self.parse)
        
        