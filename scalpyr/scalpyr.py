import anyjson as json
import requests
from bs4 import BeautifulSoup


class Scalpyr(object):

    def __init__(self, dev_key=None):
        self.base_url = "http://api.seatgeek.com/2/"
        self.dev_key = dev_key

    def get_events(self, req_args=None, event_id=None):
        return self._send_request("events", req_args, event_id)

    def get_performers(self, req_args=None, perf_id=None):
        return self._send_request("performers", req_args, perf_id)

    def get_venues(self, req_args=None, venue_id=None):
        return self._send_request("venues", req_args, venue_id)

    def get_taxonomies(self):
        return self._send_request("taxonomies", None, None)

    def get_recommendations(self, req_args=None):
        return self._send_request("recommendations", req_args, None)

    def get_tickets(self, ticket_type, json_response):
        '''
        Get ticket info based on ticket_type.
        Example for ticket_type="event":

        tickets = [
            {"event": "MF DOOM at the Apollo",
             "date": "2012-03-10T00:00:00",
             "tickets": [url1, url2, url3, ...]}
             ]
        '''
        if ticket_type == "event":
            return self._get_event_tickets(json_response)
        elif ticket_type == "performer":
            return self._get_performer_tickets(json_response)
        elif ticket_type == "venue":
            return self._get_venue_tickets(json_response)

    def _get_event_tickets(self, response):
        '''
        Take a JSON response from the SeatGeek REST API
        for an event endpoint. Then put the ticket info
        into an array of dict objects.
        '''
        ticket_urls = map(lambda x: x['url'], response['events'])
        event_titles = map(lambda x: x['title'], response['events'])
        dates = map(lambda x: x['datetime_utc'], response['events'])
        tickets = []
        for index in range(len(ticket_urls)):
            event_dict = {}
            event_dict["event"] = event_titles[index]
            event_dict["date"] = dates[index]
            event_dict["tickets"] = self._return_ticket_urls(ticket_urls[index])
            tickets.append(event_dict)
        return tickets

    def _get_performer_tickets(self, response):
        '''
        Take a JSON response from the SeatGeek REST API
        for a performer. Then put the ticket info into array of dict
        objects.
        '''
        ticket_urls = map(lambda x: x['url'], response['performers'])
        performer_name = map(lambda x: x['name'], response['performers'])
        dates = map(lambda x: x['datetime_utc'], response['performers'])
        tickets = []
        for index in range(len(ticket_urls)):
            perf_dict = {}
            performer_tickets = []
            button_urls = self._get_ticket_button_urls(ticket_urls[index])
            for url in button_urls:
                performer_tickets.extend(self._return_ticket_urls(url))
            perf_dict["performer"] = performer_name[index]
            perf_dict["date"] = dates[index]
            perf_dict["tickets"] = performer_tickets
            tickets.append(perf_dict)
        return tickets

    def _get_venue_tickets(self, response):
        '''
        Take a JSON respnse from the SeatGeek REST API
        for a venue. Then put the ticket info into array of dict
        objects.
        '''
        tickets = []
        links, dates, names = self._get_ticket_button_urls(response['url'], is_venue=True)
        for index in range(len(names)):
            venue_item = {}
            venue_item["name"] = names[index]
            venue_item["date"] = dates[index]
            venue_item["tickets"] = self._return_ticket_urls(links[index])
            tickets.append(venue_item)
        return tickets

    def _return_ticket_urls(self, sg_url):
        r = requests.get(sg_url)
        soup = BeautifulSoup(r.text)
        external_tickets = [a['href'] for a in soup.findAll('a', attrs={'class': 'select btn'})]
        return external_tickets

    def _get_ticket_button_urls(self, response, is_venue=False):
        ''' Get hrefs from ticket buttons '''
        soup = BeautifulSoup(response)
        sg_base = "http://www.seatgeek.com"
        links = [sg_base + a['href'] for a in soup.findAll('a', attrs={'class': 'ticket-button'})]
        if is_venue:
            '''
            When querying a venue page you must disambiguate since it consists
            of a table of dates with links to the specific performance.
            This information is returned as a tuple with the relevant info
            since a JSON response for a venue doesn't contain specific
            event or ticketing info.
            '''
            dates = [div.text for div in soup.findAll('div', attrs={'class': 'time'})]
            names = [span.txt for span in soup.findAll('span', attrs={'span': 'itemprop'})]
            return links, dates, names
        return links

    def _send_request(self, req_type=None, req_args=None, req_id=None):
        ''' Send a request to the SeatGeek API using requests '''
        request_string = self.base_url + "{0}/".format(req_type)
        dict_result = {}
        if req_id:
            request_string = request_string + "{0}".format(req_id)
        elif req_args:
            request_string = request_string + "?"
            for k, v in req_args.iteritems():
                request_string = request_string + "{0}={1}&".format(k, v)
            if self.dev_key is not None:
                request_string = request_string + "client_id={0}".format(self.dev_key)
        elif req_type == "taxonomies":
            request_string = request_string + "taxnonomies"
        response = requests.get(request_string)
        dict_result = json.loads(response.text)
        return dict_result
