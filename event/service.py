from event.dto import EventDTO
from event.repo import EventCSVRepo
from ai_crawler.settings import EVENT_CSV_REPO_FILE, EVENT_TXT_REPO_FILE

class EventService:
    def __init__(self, event_repository):
        self.event_repository = event_repository

    def get_event_by_uri(self, original_uri):
        return self.event_repository.get_event_by_id(original_uri)

    def create_event(self, event_data):
        return self.event_repository.create_event(event_data)

    def update_event(self, original_uri, event_data):
        return self.event_repository.update_event(original_uri, event_data)

    def delete_event(self, original_uri):
        return self.event_repository.delete_event(original_uri)

    def save(self, event_data: dict):
        # Save the DTO to the text file
        with open(EVENT_TXT_REPO_FILE, mode='a', newline='') as file:
            file.write(f"{event_data['original_uri']}\n")

        '''
        dto = EventDTO()
        dto.original_uri = event_data.get("original_uri")
        dto.title = event_data.get("title")
        dto.description = event_data.get("description")
        self.event_repository.save(dto)
        '''

event_service = EventService(event_repository=EventCSVRepo(EVENT_CSV_REPO_FILE))  # Replace with actual repository instance