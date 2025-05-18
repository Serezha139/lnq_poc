import csv
import os

from page_settings.dto import PageSettingsDTO


class PageSettingsRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.headers = [
            "page_url", "page_name", "event_list_re", "event_container_xpath",
        ]

    def save(self, dto: PageSettingsDTO):
        # Save the DTO to the CSV file
        file_exists = os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)

            # Write headers if the file is empty
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "page_url": dto.page_url,
                "page_name": dto.page_name,
                "event_list_re": dto.event_list_re,
                "event_container_xpath": dto.event_container_xpath,
            })

    def get_by_page_name(self, page_name):
        # Retrieve a DTO by page_name from the CSV file
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"!!!!Looking for page name: {page_name} in row: {row}")
                if row["page_name"] == page_name:
                    dto = PageSettingsDTO()
                    dto.page_url = row["page_url"]
                    dto.page_name = row["page_name"]
                    dto.event_list_re = row["event_list_re"]
                    dto.event_container_xpath = row["event_container_xpath"]
                    return dto
        return None

    def update(self, dto: PageSettingsDTO):
        # Update the DTO in the CSV file
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["page_name"] == dto.page_name:
                    row = {
                        "page_url": dto.page_url,
                        "page_name": dto.page_name,
                        "event_list_re": dto.event_list_re,
                        "event_container_xpath": dto.event_container_xpath,
                    }
                rows.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)

    def delete_by_page_name(self, page_name):
        # Read all rows from the CSV file
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["page_name"] != page_name:
                    rows.append(row)

        # Write the remaining rows back to the CSV file
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(rows)