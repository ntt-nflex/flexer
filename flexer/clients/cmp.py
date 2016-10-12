import requests
import json


class CmpClient(object):
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth
        self._headers = {'User-Agent': 'nflex-client'}
        self._cookie_jar = requests.cookies.RequestsCookieJar()

    def use_access_token(self, access_token=None):
        """Use an access token when sending requests to CMP."""
        if not access_token:
            self._cookie_jar.clear()
            return

        self._cookie_jar.set('x-cmp-op',
                             access_token.get("value"),
                             path=access_token.get("path"))

    def url(self, path):
        """Construct an endpoint path using the CMP base URL.

        Args:
            path (str): The path to use

        Returns:
            str: The full CMP API endpoint path
        """
        return self._url + path

    def get(self, path, params=None):
        """Execute a GET request.

        Args:
            path (str): The CMP API endpoint path
            params (dict): Dict with the GET request parameters

        Returns:
            requests.Response: The response of the request
        """
        return requests.get(self.url(path),
                            params=params,
                            auth=self._auth,
                            headers=self._headers,
                            cookies=self._cookie_jar)

    def post(self, path, data):
        """Execute a POST request.

        Args:
            path (str): The CMP API endpoint path
            data (dict): Dict with the POST request payload

        Returns:
            requests.Response: The response of the request
        """
        return requests.post(self.url(path),
                             json=data,
                             auth=self._auth,
                             headers=self._headers,
                             cookies=self._cookie_jar)

    def post_file(self, path, zip_file):
        """Execute a POST request.

        Args:
            path (str): The CMP API endpoint path
            zip_file (file): A zipfile to upload

        Returns:
            requests.Response: The response of the request
        """
        files = {
            'file': ('temp_module.zip', zip_file)
        }
        return requests.post(self.url(path),
                             files=files,
                             auth=self._auth,
                             headers=self._headers,
                             cookies=self._cookie_jar)

    def put(self, path, data):
        """Execute a PUT request.

        Args:
            path (str): The CMP API endpoint path
            data (dict): Dict with the PUT request payload

        Returns:
            requests.Response: The response of the request
        """
        return requests.put(url=self.url(path),
                            data=json.dumps(data),
                            auth=self._auth,
                            headers=self._headers,
                            cookies=self._cookie_jar)

    def patch(self, path, data):
        """Execute a PATCH request.

        Args:
            path (str): The CMP API endpoint path
            data (dict): Dict with the PUT request payload

        Returns:
            requests.Response: The response of the request
        """
        return requests.patch(self.url(path),
                              data=json.dumps(data),
                              auth=self._auth,
                              headers=self._headers,
                              cookies=self._cookie_jar)
