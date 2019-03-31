import copy

import requests

from urllib.parse import urlparse


class TwitchClient:
    """ This is a basic Twitch Client instance that interfaces with the New Twitch API. """

    # The Base URL of the New Twitch API.
    API_BASE_URL = "https://api.twitch.tv"

    def __init__(self, key):
        """ Creates a new TwitchClient instance with the given API key. """

        self.api_key = key
        self.base_url = urlparse(self.API_BASE_URL)

    def get(self, path, **kwargs):
        """Performs a GET request to the new Twitch API endpoint at the given
        path, while passing along the kwargs to the requests.get method.

        Parameters:
            path (str): The API request path

        Returns:
            response: requests response object
        """
        headers = {'Client-ID': self.api_key}

        if 'headers' in kwargs:
            kwargs['headers'] = {**headers, **kwargs['headers']}
        else:
            kwargs['headers'] = headers

        url = copy.copy(self.base_url)
        url = url._replace(path=path)

        res = requests.get(url.geturl(), **kwargs)

        return res

    def get_streams(self, params):
        """Requests a list of streams while passing params as the query."""

        res = self.get('/helix/streams', params=params)

        return res.json()

