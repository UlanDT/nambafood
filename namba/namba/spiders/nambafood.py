# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import NambaItem


class NambafoodSpider(scrapy.Spider):

    name = 'nambafood'

    start_urls = ['https://nambafood.kg/cafe']

    def parse(self, response):

        all_links = response.css("a.cafe-item::attr(href)").extract()
        urls = ["https://nambafood.kg" + i for i in all_links]
        print(len(urls))
        for i in urls:
            yield response.follow(i, callback=self.parse)

        print(response)

        items = NambaItem()

        cafe_name = response.css(".cafe--name::text")[0].extract().strip()
        cafe_image_url = response.css(".prev--thumb img").xpath("@src")[0].extract()
        cafe_background_style = response.xpath("//div[contains(@class, 'card--background')]//@style")[0].extract().strip()
        cafe_background_image_url = "https://nambafood.kg"+''.join(re.findall('\/\w+', cafe_background_style))
        average_price = response.css(".information--item--description::text")[0].extract().split()[0] + " сом"
        delivery_price = response.css(".information--item--description::text")[1].extract().split()[0] + " сом"
        working_hours = response.xpath("//div[contains(@class, 'information--item--description')]/text()")[3].extract().strip()
        address = response.css(".map-address--text::text")[1].extract().strip()
        phone = response.css(".map-address--text::text")[3].extract().strip()
        parent_categories_get = response.css('.tag-list__tag::text').extract()
        parent_categories = [i.strip() for i in parent_categories_get]
        longitude = response.css("div.map a::attr(href)").extract()
        latitude = response.css("div.map > a")

        """
        Section for scraping restaurant menu
        """
        spans = response.css("span.section--container")  # 13
        categories = {}
        for span in spans:
            category_name = span.css("h2.title::text").get().strip()
            card_items = span.css("div.card--item")
            dish_info = {}
            for card_item in card_items:

                if any(card_item.css("div.card--item--title::text").getall()):
                    dish_title = card_item.css("div.card--item--title::text").getall()[0].strip()
                else:
                    continue

                dish_price = card_item.css("div.price::text").extract()[0].strip()
                dish_image_url = card_item.css('.card--item--prev img::attr(src)').extract_first()
                dish_description = card_item.css(".card--item--description::text")[0].extract().strip()
                dish_info.update({dish_title: {'dish_price': dish_price,
                                               "dish_image_url": "https://nambafood.kg"+dish_image_url,
                                               "dish_description": dish_description}})
            categories.update({category_name: dish_info})

        """
        Section to scrape reviews
        """
        all_reviews = response.css(".feedback--comment-wrap")
        reviews = {}

        for review in all_reviews:
            try:
                reviewed_user = review.css("span.name::text")[0].extract()
                reviewed_date = review.css("span.date::text")[0].extract()
                review_text = review.css("div.comment--text::text")[0].extract().strip()

                reviews.update({"reviewed_user": reviewed_user,
                                "reviewed_date": reviewed_date,
                                "review_text": review_text})
            except IndexError:
                continue

        items['cafe_name'] = cafe_name
        items['cafe_image_url'] = cafe_image_url
        items['cafe_background_image_url'] = cafe_background_image_url
        items['average_price'] = average_price
        items['delivery_price'] = delivery_price
        items['working_hours'] = working_hours
        items['address'] = address
        items['phone'] = phone
        items['categories'] = categories
        items['reviews'] = reviews
        items['longitude'] = longitude
        items['latitude'] = latitude
        items['parent_categories'] = parent_categories

        yield items

