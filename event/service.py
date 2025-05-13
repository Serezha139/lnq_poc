from event.dto import EventDTO
from event.repo import EventCSVRepo
from ai_crawler.settings import EVENT_CSV_REPO_FILE, EVENT_TXT_REPO_FILE


def safe_extract_text(element, xpath):
    """
    Safely extract text from an element using XPath.
    """
    try:
        return element.xpath(xpath)[0].get('text', None) if element.xpath(xpath) else None
    except Exception as e:
        print(f"Error extracting text with XPath '{xpath}': {e}")
        return None


class EventService:
    def __init__(self, event_repository):
        self.event_repository = event_repository

    def create_event(self, title, description, link, city, country, address,
                     google_maps_uri, start_date, end_date, cover):
        # Create a new event
        event = EventDTO(
            title=title,
            description=description,
            link=link,
            city=city,
            country=country,
            address=address,
            google_maps_uri=google_maps_uri,
            start_date=start_date,
            end_date=end_date,
            cover=cover
        )
        self.event_repository.save(event)


event_service = EventService(event_repository=EventCSVRepo(EVENT_CSV_REPO_FILE))  # Replace with actual repository instance