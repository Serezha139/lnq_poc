import asyncio

import scrapy
from page_settings.dto import PageSettingsDTO
from page_settings.service import page_settings_service
import json
import os
from event.service import event_service
from ai.ai_service import openai_service
import ai_crawler.settings as settings
from ai_crawler.spider_utils import load_page_content
from lxml import html


class ArtBaselSpider(scrapy.Spider):
    name = "artbasel"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.starting_url = settings.STARTING_URL_DICT.get("artbasel")

    def start_requests(self):
        yield scrapy.Request(
            url=self.starting_url,
            callback=self.parse_starting_page,
                meta={"playwright": True, "playwright_include_page": True}
        )

    async def parse_starting_page(self, response):
        page_settings = page_settings_service.get_page_settings_by_name(self.name)
        content = await load_page_content(response)
        html_content = html.fromstring(content)
        if not page_settings:
            event_list_xpath = openai_service.get_event_list_xpath_expression(content)
            page_settings = PageSettingsDTO()
            page_settings.page_url = response.url
            page_settings.page_name = self.name
            page_settings.event_list_xpath = event_list_xpath
            page_settings_service.save_page_settings(
                dto=page_settings
            )

        # Follow links using event_list_xpath
        event_links = html_content.xpath(page_settings.event_list_xpath)
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Event links: {event_links} from xpath: {page_settings.event_list_xpath}")
        for link in event_links:
            yield response.follow(
                link.get("href"),
                callback=self.parse_event_page,
                meta={"page_name": self.name, "playwright": True, "playwright_include_page": True}
            )

    async def parse_event_page(self, response):
        await asyncio.sleep(1)
        page_settings = page_settings_service.get_page_settings_by_name(self.name)
        content = await load_page_content(response)
        html_content = html.fromstring(content)
        if not page_settings.event_container_xpath:
            # Dynamically determine the event_container_xpath
            page_settings.event_container_xpath = openai_service.get_event_container_xpath_expression(content)
            page_settings_service.update_page_settings(dto=page_settings)

        # Extract and process event data
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Event container xpath: {page_settings.event_container_xpath}")
        event_data = html_content.xpath(page_settings.event_container_xpath)[0].get("text")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Event data: {event_data} from xpath: {page_settings.event_container_xpath}")
        if event_data:
            self.save_event_data(event_data)
    def save_event_data(self, event_data):
        # Save event data to a JSON file
        event_data = json.loads(event_data)
        event_service.save(event_data)