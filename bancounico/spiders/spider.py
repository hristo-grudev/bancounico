import scrapy

from scrapy.loader import ItemLoader

from ..items import BancounicoItem
from itemloaders.processors import TakeFirst


class BancounicoSpider(scrapy.Spider):
	name = 'bancounico'
	start_urls = ['https://www.bancounico.co.mz/banco-unico/sala-imprensa/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="middle_content"]')
		for post in post_links:
			title = post.xpath('.//div[@class="title_content"]/text()').get()
			description = post.xpath('.//div[@class="body_content"]//text()[normalize-space() and not(ancestor::strong)]').getall()
			description = [p.strip() for p in description if '{' not in p]
			description = ' '.join(description).strip()
			date = post.xpath('//strong/span/text()').get()

			item = ItemLoader(item=BancounicoItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
