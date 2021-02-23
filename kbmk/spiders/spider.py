import scrapy

from scrapy.loader import ItemLoader
from ..items import KbmkItem
from itemloaders.processors import TakeFirst


class KbmkSpider(scrapy.Spider):
	name = 'kbmk'
	start_urls = ['https://www.kb.com.mk/Default.aspx?sel=1000&lang=1&uc=10&par=1988']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@id="printableContent"]//text()[normalize-space() and not(ancestor::h1 | ancestor::script)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=KbmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
