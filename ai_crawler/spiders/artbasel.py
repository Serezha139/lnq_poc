import re

import scrapy
from scrapy.utils.response import get_base_url

from lxml import html, etree
from scrapy import Spider
from event.service import event_service
from page_settings.service import page_settings_service
from ai_crawler import settings
from ai_crawler.spider_utils import load_page_content, extract_links_from_element, safe_extract


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
        event_links = [link for link in links if filter_re.match(link) and link != response.url]
        for link in event_links[:1]:
            yield response.follow(
                link,
                callback=self.parse_event_page,
                meta={"playwright": True, "playwright_include_page": True}
            )

    async def parse_event_page(self, response):
        # This method will be implemented in the next step
        page_settings = page_settings_service.get_page_settings_by_name(self.name)
        content = await load_page_content(response)
        html_content = html.fromstring(content)
        container_html = html_content.xpath(page_settings.event_container_xpath)[0]
        print(f"Container HTML: {etree.tostring(container_html, pretty_print=True).decode('utf-8')}")
        event_link = response.url
        event_title = safe_extract(container_html, page_settings.title_xpath, default="No title found")
        event_description = safe_extract(container_html, page_settings.description_xpath, default="No description found")
        event_image = safe_extract(container_html, page_settings.cover_xpath, default="No image found")
        event_google_maps_uri = safe_extract(container_html, page_settings.google_maps_uri_xpath, default="No Google Maps URI found")
        event_city = safe_extract(container_html, page_settings.city_xpath, default="No city found")
        event_country = safe_extract(container_html, page_settings.country_xpath, default="No country found")
        event_address = safe_extract(container_html, page_settings.address_xpath, default="No address found")
        event_start_date = safe_extract(container_html, page_settings.start_date_xpath, default="No start date found")
        event_end_date = safe_extract(container_html, page_settings.end_date_xpath, default="No end date found")

        event_service.create_event(
            title=event_title,
            description=event_description,
            link=event_link,
            city=event_city,
            country=event_country,
            address=event_address,
            google_maps_uri=event_google_maps_uri,
            start_date=event_start_date,
            end_date=event_end_date,
            cover=event_image,
        )