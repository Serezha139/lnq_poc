import re

import scrapy
from scrapy.utils.response import get_base_url

from lxml import html, etree
from scrapy import Spider
from event.service import event_service
from page_settings.service import page_settings_service
from ai_crawler import settings
from ai_crawler.spider_utils import load_page_content, extract_links_from_element, safe_extract
from ai.ai_service import openai_service


class ArtbaselSpider(Spider):
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
        # This method will be implemented in the next step
        page_settings = page_settings_service.get_page_settings_by_name(self.name)
        page_content = await load_page_content(response)
        html_content = html.fromstring(page_content)
        base_url = get_base_url(response)
        links = extract_links_from_element(html_content, base_url=base_url)
        filter_re = re.compile(page_settings.event_list_re)
        event_links = {link for link in links if filter_re.match(link) and link != response.url}
        print(f"Event links: {event_links} from re: {page_settings.event_list_re}")
        print(f"Event links count: {len(event_links)}")
        for link in event_links:
            yield response.follow(
                link,
                callback=self.parse_event_page,
                meta={"playwright": True, "playwright_include_page": True}
            )

    async def parse_event_page(self, response):
        # This method will be implemented in the next step
        try:
            page_settings = page_settings_service.get_page_settings_by_name(self.name)
            content = await load_page_content(response)
            html_content = html.fromstring(content)
            container_html = html_content.xpath(page_settings.event_container_xpath)[0]
            str_html = etree.tostring(container_html, pretty_print=True).decode("utf-8")
            event_data = openai_service.get_event_json(str_html)

            event_dto = event_service.from_dict(event_data)
            event_dto.original_uri = response.url
            event_dto.original_site = self.name
            event_service.save_event(event_dto)
        except Exception as e:
            print(f"Error parsing event page: {e}")
            print(f"Response URL: {response.url}")
            if event_data:
                print(f"Event data: {event_data}")
