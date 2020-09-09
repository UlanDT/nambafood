# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import NambaItem



class NambafoodSpider(scrapy.Spider):

    name = 'nambafood'

    start_urls = ['https://nambafood.kg/dominopizza']

    def parse(self, response):

        items = NambaItem

        cafe_name = response.css(".cafe--name::text")[0].extract().strip()
        cafe_image_url = response.css(".prev--thumb img").xpath("@src")[0].extract()
        cafe_background_style = response.xpath("//div[contains(@class, 'card--background')]//@style")[0].extract().strip()
        cafe_background_image_url = "https://nambafood.kg"+''.join(re.findall('\/\w+', cafe_background_style))
        average_price = response.css(".information--item--description::text")[0].extract().split()[0] + " сом"
        delivery_price = response.css(".information--item--description::text")[1].extract().split()[0] + " сом"
        working_hours = response.xpath("//div[contains(@class, 'information--item--description')]/text()")[3].extract().strip()
        address = response.css(".map-address--text::text")[1].extract().strip()
        phone = response.css(".map-address--text::text")[3].extract().strip()
        # latitude = response.css("div.map a::attr(href)").extract()

        spans = response.css("span.section--container")  # 13
        categories = {}
        dish_info = {}
        for span in spans:
            category_name = span.css("h2.title::text").get().strip()
            card_items = span.css("div.card--item")

            for card_item in card_items:

                if any(card_item.css("div.card--item--title::text").getall()):
                    dish_title = card_item.css("div.card--item--title::text").getall()[0].strip()
                else:
                    continue

                dish_price = card_item.css("div.price::text").extract()[0].strip()

                dish_info.update({category_name: {dish_title: {'dish_price': dish_price}}})
                print(dish_info)
            # print(dish_info)
            categories.update(dish_info)


        yield ({"cafe_name": cafe_name,
                "cafe_image_url": "https://nambafood.kg" + cafe_image_url,
                "cafe_background_image_url": cafe_background_image_url,
                "average_price": average_price,
                "delivery_price": delivery_price,
                "working_hours": working_hours,
                "address": address,
                "phone": phone,
                "latitude": "latitude",
                "categories": categories})
        # items['cafe_name'] = cafe_name
        # items['cafe_image'] = cafe_image
        #
        # yield items
        # all_restaurant_titles = response.css('div.cafe--name::text').extract()
        #
        # items['title'] = all_restaurant_titles
        # # items['author'] = author
        # yield {'restaurant_title': all_restaurant_titles}



        # yield response.follow(links, callback=_self.parse)
        # yield items
        # scrapy crawl quotes -o items.json save them in json file
# response.xpath("//div[@class='cafe--name']/text()")[0].extract()
# response.css("div.catalog-wrap a").xpath("@href").extract()
# response.css("a").xpath("@href").extract()  all links