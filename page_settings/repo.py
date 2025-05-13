import csv
import os

from page_settings.dto import PageSettingsDTO


class PageSettingsRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.headers = [
            "page_url", "page_name", "event_list_re", "event_container_xpath",
            "cover_xpath", "thumb_xpath", "title_xpath", "description_xpath", "link_xpath",
            "city_xpath", "country_xpath", "address_xpath", "lat_xpath", "lng_xpath",
            "google_maps_uri_xpath", "start_date_xpath", "end_date_xpath", "dates_xpath",
            "allDay_xpath", "timeFrom_xpath", "timeTill_xpath"
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
                "cover_xpath": dto.cover_xpath,
                "thumb_xpath": dto.thumb_xpath,
                "title_xpath": dto.title_xpath,
                "description_xpath": dto.description_xpath,
                "link_xpath": dto.link_xpath,
                "city_xpath": dto.city_xpath,
                "country_xpath": dto.country_xpath,
                "address_xpath": dto.address_xpath,
                "lat_xpath": dto.lat_xpath,
                "lng_xpath": dto.lng_xpath,
                "google_maps_uri_xpath": dto.google_maps_uri_xpath,
                "start_date_xpath": dto.start_date_xpath,
                "end_date_xpath": dto.end_date_xpath,
                "dates_xpath": dto.dates_xpath,
                "allDay_xpath": dto.allDay_xpath,
                "timeFrom_xpath": dto.timeFrom_xpath,
                "timeTill_xpath": dto.timeTill_xpath,
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
                    dto.cover_xpath = row["cover_xpath"]
                    dto.thumb_xpath = row["thumb_xpath"]
                    dto.title_xpath = row["title_xpath"]
                    dto.description_xpath = row["description_xpath"]
                    dto.link_xpath = row["link_xpath"]
                    dto.city_xpath = row["city_xpath"]
                    dto.country_xpath = row["country_xpath"]
                    dto.address_xpath = row["address_xpath"]
                    dto.lat_xpath = row["lat_xpath"]
                    dto.lng_xpath = row["lng_xpath"]
                    dto.google_maps_uri_xpath = row["google_maps_uri_xpath"]
                    dto.start_date_xpath = row["start_date_xpath"]
                    dto.end_date_xpath = row["end_date_xpath"]
                    dto.dates_xpath = row["dates_xpath"]
                    dto.allDay_xpath = row["allDay_xpath"]
                    dto.timeFrom_xpath = row["timeFrom_xpath"]
                    dto.timeTill_xpath = row["timeTill_xpath"]
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
                        "cover_xpath": dto.cover_xpath,
                        "thumb_xpath": dto.thumb_xpath,
                        "title_xpath": dto.title_xpath,
                        "description_xpath": dto.description_xpath,
                        "link_xpath": dto.link_xpath,
                        "city_xpath": dto.city_xpath,
                        "country_xpath": dto.country_xpath,
                        "address_xpath": dto.address_xpath,
                        "lat_xpath": dto.lat_xpath,
                        "lng_xpath": dto.lng_xpath,
                        "google_maps_uri_xpath": dto.google_maps_uri_xpath,
                        "start_date_xpath": dto.start_date_xpath,
                        "end_date_xpath": dto.end_date_xpath,
                        "dates_xpath": dto.dates_xpath,
                        "allDay_xpath": dto.allDay_xpath,
                        "timeFrom_xpath": dto.timeFrom_xpath,
                        "timeTill_xpath": dto.timeTill_xpath,
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