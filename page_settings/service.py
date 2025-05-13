from page_settings.dto import PageSettingsDTO
from page_settings.repo import PageSettingsRepository
from ai_crawler.settings import PAGE_SETTINGS_FILE


class PageSettingsService:
    def __init__(self, repository: PageSettingsRepository):
        self.repository = repository

    def save_page_settings(self, dto: PageSettingsDTO):
        # Create a DTO and save it using the repository

        self.repository.save(dto)

    def get_page_settings_by_name(self, page_name) -> PageSettingsDTO:
        # Retrieve a DTO by page_name using the repository
        return self.repository.get_by_page_name(page_name)

    def populate_page_settings(self, page_settings: PageSettingsDTO, data: dict):
        # Populate the DTO with data
        print(f"Populating page settings with data: {data}")
        page_settings.cover_xpath = data.get("cover")
        page_settings.thumb_xpath = data.get("thumb")
        page_settings.title_xpath = data.get("title")
        page_settings.description_xpath = data.get("description")
        page_settings.link_xpath = data.get("link")
        page_settings.city_xpath = data.get("city")
        page_settings.country_xpath = data.get("country")
        page_settings.address_xpath = data.get("address")
        page_settings.lat_xpath = data.get("lat")
        page_settings.lng_xpath = data.get("lng")
        page_settings.google_maps_uri_xpath = data.get("google_maps_uri")
        page_settings.start_date_xpath = data.get("start_date")
        page_settings.end_date_xpath = data.get("end_date")
        page_settings.dates_xpath = data.get("dates")
        page_settings.timeFrom_xpath = data.get("timeFrom")
        # Populate the DTO with data from the dictionary

        # Save the populated DTO
        self.repository.save(page_settings)

    def delete_by_name(self, page_name):
        # Delete a DTO by page_name using the repository
        self.repository.delete_by_page_name(page_name)

    def update(self, dto):
        # Update a DTO by page_name using the repository
        self.repository.update(dto)


page_settings_service = PageSettingsService(repository=PageSettingsRepository(file_path=PAGE_SETTINGS_FILE))
