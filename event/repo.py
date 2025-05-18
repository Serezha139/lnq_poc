import csv
import json
import os
import datetime

from event.dto import EventDTO


def remove_bad_symbols_from_uri(uri):
    """
    remove bad symbols from uri
    :param uri:
    :return:
    """
    bad_symbols = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for symbol in bad_symbols:
        uri = uri.replace(symbol, '_')
    return uri

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

class EventJsonRepo:
    """
    class to save eventDTO to json file
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, dto: EventDTO):
        event_dict = {
            "original_uri": dto.original_uri,
            "title": dto.title,
            "description": dto.description or "",
            "start_datetime": dto.start_datetime,
            "end_datetime": dto.end_datetime,
            "dates": dto.dates,
            "city": dto.city,
            "country": dto.country,
            "address": dto.address,
            "google_maps_uri": dto.google_maps_uri,
            "cover": dto.cover,
            "thumb": dto.thumb,
            "link": dto.link,
            "original_site": dto.original_site
        }
        # create a file with a name of dto.original_site and todays_date
        # create a directory with a site name
        directory = f"events/{dto.original_site}_{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = f"{dto.title}______{remove_bad_symbols_from_uri(dto.original_uri)}.json"
        filepath = os.path.join(directory, file_name)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(event_dict, file, indent=4)
            file.write('\n')
