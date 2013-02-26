import json
import requests


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


