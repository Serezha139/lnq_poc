import csv

from event.dto import EventDTO


class EventCSVRepo:
    """
    class to save eventDTO to csv file
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, dto: EventDTO):
        # Save the DTO to the CSV file. If exists then rewrite it
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
            for row in rows:
                if row[0] == dto.original_uri:
                    # If the event already exists, update it
                    row[1] = dto.title
                    row[2] = dto.description
                    break

        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
            # Write the new event if it doesn't exist
            if not any(row[0] == dto.original_uri for row in rows):
                writer.writerow([dto.original_uri, dto.title, dto.description, dto.start_date])
