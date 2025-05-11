class EventDTO:
    def __init__(self):
        self.original_site = None
        self.original_uri = None
        self._id = None
        self.cover = None
        self.thumb = None
        self.title = None
        self.description = None
        self.link = None
        # location attributes
        self.city = None
        self.country = None
        self.address = None
        self.lat = None
        self.lng = None
        self.google_maps_uri = None
        # date
        self.start_date = None
        self.end_date = None
        self.dates = []
        # time
        self.allDay = False
        self.timeFrom = None
        self.timeTill = None
