class PageSettingsDTO:
    def __init__(self):
        self.page_url = None
        self.page_name = None
        self.event_list_re = None
        self.event_container_xpath = None

        # XPath fields for EventDTO
        self.cover_xpath = None
        self.thumb_xpath = None
        self.title_xpath = None
        self.description_xpath = None
        self.link_xpath = None
        self.city_xpath = None
        self.country_xpath = None
        self.address_xpath = None
        self.lat_xpath = None
        self.lng_xpath = None
        self.google_maps_uri_xpath = None
        self.start_date_xpath = None
        self.end_date_xpath = None
        self.dates_xpath = None
        self.allDay_xpath = None
        self.timeFrom_xpath = None
        self.timeTill_xpath = None
