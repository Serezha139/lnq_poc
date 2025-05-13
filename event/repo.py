import csv
import os

from event.dto import EventDTO


class EventCSVRepo:
    """
    class to save eventDTO to csv file
    """
    def __init__(self, file_path):
        self.file_path = file_path


    def save(self, dto: EventDTO):
        # Define the field names (headers)
        field_names = [
            "original_uri", "title", "description", "start_date", "end_date", "dates",
            "allDay", "timeFrom", "timeTill", "city", "country", "address",
            "google_maps_uri", "cover", "thumb", "link", "original_site"
        ]

        # Check if the file exists and is not empty
        file_exists = os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)

            # Write headers if the file is empty
            if not file_exists:
                writer.writeheader()

            # Write the DTO data as a row
            writer.writerow({
                "original_uri": dto.original_uri,
                "title": dto.title,
                "description": dto.description,
                "start_date": dto.start_date,
                "end_date": dto.end_date,
                "dates": dto.dates,
                "allDay": dto.allDay,
                "timeFrom": dto.timeFrom,
                "timeTill": dto.timeTill,
                "city": dto.city,
                "country": dto.country,
                "address": dto.address,
                "google_maps_uri": dto.google_maps_uri,
                "cover": dto.cover,
                "thumb": dto.thumb,
                "link": dto.link,
                "original_site": dto.original_site,
            })

