import re

import scrapy
from scrapy.utils.response import get_base_url
from page_settings.dto import PageSettingsDTO
from page_settings.service import page_settings_service
from ai.ai_service import openai_service
import ai_crawler.settings as settings
from ai_crawler.spider_utils import load_page_content, extract_links_from_element
from lxml import html


class ArtBaselWarmupSpider(scrapy.Spider):
    name = "artbasel_warmup"
    site_name = "artbasel"

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
        page_settings = page_settings_service.get_page_settings_by_name(self.site_name)
        page_content = await load_page_content(response)
        html_content = html.fromstring(page_content)
        base_url = get_base_url(response)
        all_links = extract_links_from_element(html_content, base_url=base_url)
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!All links: {all_links}")
        if not page_settings:
            event_list_re = openai_service.get_event_list_re_expression(all_links)
            page_settings = PageSettingsDTO()
            page_settings.page_url = response.url
            page_settings.page_name = self.site_name
            page_settings.event_list_re = event_list_re
            page_settings_service.save_page_settings(
                dto=page_settings
            )

        # Follow links using event_list_re
        filter_re = re.compile(page_settings.event_list_re)
        event_links = [link for link in all_links if filter_re.match(link) and link != response.url]
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Event links: {event_links} from re: {page_settings.event_list_re}")
        if not event_links:
            page_settings_service.delete_by_name(
                page_name=page_settings.page_name
            )
        else:
            page_settings_service.update(
                dto=page_settings
            )
        for link in event_links[:2]:
            yield response.follow(
                link,
                callback=self.parse_event_page,
                meta={"page_name": self.name, "playwright": True, "playwright_include_page": True}
            )

    async def parse_event_page(self, response):
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Event page: {response.url}")
        page_settings = page_settings_service.get_page_settings_by_name(self.site_name)
        content = await load_page_content(response)
        html_content = html.fromstring(content)
        # Dynamically determine the event_container_xpath
        xpath_event_container = openai_service.get_event_container_xpath_expression(content)
        page_settings.event_container_xpath = xpath_event_container
        container_html = html_content.xpath(page_settings.event_container_xpath)[0]
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Container html: {container_html}")
        for key, value in page_settings.gpt_request_field_mapping.items():
            xpath = openai_service.get_event_xpath_expressions(container_html, key)
            setattr(page_settings, value, xpath)
        page_settings_service.save_page_settings(page_settings)
