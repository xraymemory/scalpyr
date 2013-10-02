from datetime import datetime
import anyjson as json
from mock import patch
from unittest import TestCase

from scalpyr import Scalpyr, requests


class TestScalpyr(TestCase):
    def test_send_request(self):
        with patch.object(requests, 'get') as get:
            scalpyr = Scalpyr()
            get.return_value.text = json.dumps(dict(testing='test'))
            get.return_value.status_code = 200

            results = scalpyr._send_request('testing', dict(testing='test'))

            get.assert_called_with('http://api.seatgeek.com/2/testing/?testing=test&')
            self.assertEqual(results['testing'], 'test')

    def test_send_request_with_key(self):
        with patch.object(requests, 'get') as get:
            scalpyr = Scalpyr(dev_key=1234)
            get.return_value.text = json.dumps(dict(testing='test'))
            get.return_value.status_code = 200

            results = scalpyr._send_request('testing', dict(testing='test'))

            get.assert_called_with('http://api.seatgeek.com/2/testing/?testing=test&client_id=1234')
