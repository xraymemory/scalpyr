import json
import requests
from BeautifulSoup import BeautifulSoup


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
        if ticket_type == "event":
            return self._get_event_tickets(json_response)
        elif ticket_type == "performer":
            return self._get_performer_tickets(json_response)
        elif ticket_type == "venue":
            pass

    def _get_event_tickets(self, response):
        ticket_urls = map(lambda x: x['url'], response['events'])
        event_titles = map(lambda x: x['title'], response['events'])
        tickets = []
        for index in range(len(ticket_urls)):
            event_dict = {}
            r = requests.get(ticket_urls[index])
            soup = BeautifulSoup(r.text)
            external_tickets = [a['href'] for a in soup.findAll('a', attrs={'class': 'select btn'})]
            event_dict["event"] = event_titles[index]
            event_dict["tickets"] = external_tickets
            tickets.append(event_dict)
        return tickets

    def _get_performer_tickets(self, response):
        ticket_urls = map(lambda x: x['url'], response['performers'])
        performer_name = map(lambda x: x['name'], response['performers'])
        tickets = []
        for index in range(len(ticket_urls)):
            perf_dict = {}
            performer_list = []
            button_urls = self._get_ticket_button_urls(ticket_urls[index])
            for url in button_urls:
                r = requests.get(ticket_urls[index])
                soup = BeautifulSoup(r.text)
                external_tickets = [a['href'] for a in soup.findAll('a', attrs={'class': 'select btn'})]
                performer_list.extend(external_tickets)
            perf_dict["performer"] = performer_name[index]
            perf_dict["tickets"] = external_tickets
            tickets.append(perf_dict)
        return tickets

    def _get_ticket_button_urls(self, response):
        soup = BeautifulSoup(response)
        sg_base = "http://www.seatgeek.com"
        links = [sg_base + a['href'] for a in soup.findAll('a', attrs={'class': 'ticket-button'})]
        return links

    def _send_request(self, req_type=None, req_args=None, req_id=None):
        request_string = self.base_url + "{0}/".format(req_type)
        dict_result = {}
        if req_id:
            request_string = request_string + "{0}".format(req_id)
        elif req_args:
            request_string = request_string + "?"
            for k, v in req_args.iteritems():
                request_string = request_string + "{0}={1}&".format(k, v)
            if self.dev_key != None:
                request_string = request_string + "client_id={0}".format(self.dev_key)
        elif req_type == "taxonomies":
            request_string = request_string + "taxnonomies"
        response = requests.get(request_string)
        dict_result = json.loads(response.text)
        return dict_result


