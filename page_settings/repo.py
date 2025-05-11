import csv
from page_settings.dto import PageSettingsDTO


class PageSettingsRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, dto: PageSettingsDTO):
        # Save the DTO to the CSV file
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                dto.page_url,
                dto.page_name,
                dto.event_list_xpath,
                dto.event_list_css,
                dto.event_container_xpath
            ])

    def get_by_page_name(self, page_name):
        # Retrieve a DTO by page_name from the CSV file
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == page_name:  # Assuming page_name is the second column
                    dto = PageSettingsDTO()
                    dto.page_url = row[0]
                    dto.page_name = row[1]
                    dto.event_list_xpath = row[2]
                    dto.event_list_css = row[3]
                    dto.event_container_xpath = row[4]
                    return dto
        return None

    def update(self, dto: PageSettingsDTO):
        # Update the DTO in the CSV file
        rows = []
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == dto.page_name:
                    row[0] = dto.page_url
                    row[1] = dto.page_name
                    row[2] = dto.event_list_xpath
                    row[3] = dto.event_list_css
                    row[4] = dto.event_container_xpath
                rows.append(row)
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)