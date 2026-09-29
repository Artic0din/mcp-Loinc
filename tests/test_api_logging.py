import base64
import logging
import unittest
from unittest import mock

import requests

from loinc_api.api import LOINCAPI

USERNAME = "user"
PASSWORD = "s3cret-pass"


def fake_get(url, auth, headers, params):
    request = requests.Request("GET", url, auth=auth, headers=headers, params=params).prepare()
    response = requests.Response()
    response.status_code = 200
    response._content = b'{"Results": []}'
    response.request = request
    return response


class CredentialLoggingTest(unittest.TestCase):
    def test_request_logs_do_not_contain_credentials(self):
        api = LOINCAPI(USERNAME, PASSWORD)
        encoded = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

        with mock.patch("loinc_api.api.requests.get", side_effect=fake_get), \
                self.assertLogs("loinc_api.api", level=logging.DEBUG) as logs:
            api.search_loincs("hemoglobin")

        output = "\n".join(logs.output)
        self.assertNotIn(encoded, output)
        self.assertNotIn(PASSWORD, output)
        self.assertNotIn("Authorization", output)


if __name__ == "__main__":
    unittest.main()
