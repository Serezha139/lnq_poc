class EventDTO:
    def __init__(self, title=None, description=None, link=None, city=None, country=None,
                 address=None, google_maps_uri=None, start_date=None, end_date=None, allDay=False,
                 timeFrom=None, timeTill=None, dates=None, original_site=None, original_uri=None,
                 cover=None, thumb=None):
        self.title = title
        self.description = description
        self.link = link
        self.city = city
        self.country = country

        self.address = address
        self.google_maps_uri = google_maps_uri
        self.start_date = start_date
        self.end_date = end_date
        self.allDay = allDay
        self.timeFrom = timeFrom
        self.timeTill = timeTill
        self.dates = dates
        self.original_site = original_site
        self.original_uri = original_uri
        self.cover = cover
        self.thumb = thumb

