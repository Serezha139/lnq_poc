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

    def delete_by_name(self, page_name):
        # Delete a DTO by page_name using the repository
        self.repository.delete_by_page_name(page_name)

    def update(self, dto):
        # Update a DTO by page_name using the repository
        self.repository.update(dto)


page_settings_service = PageSettingsService(repository=PageSettingsRepository(file_path=PAGE_SETTINGS_FILE))
