import os
import time
import logging

import toml
import requests

from twitch_client import TwitchClient


class TwitchRecorder:
    DEFAULT_CHECK_INTERVAL = 30

    # Constructs a new TwitchRecorder instance.
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    # Loads the TOML file at the given +path+ and uses it as a config file.
    def load_config(self, path):
        config = toml.load(path)

        self.config = config
        self.config_path = path
        self.check_interval = config['twitch'].get(
                'check_interval', self.DEFAULT_CHECK_INTERVAL)
        twitch_api_key = config['twitch'].get(
                'key', os.environ.get('TWITCH_API_KEY'))
        self.twitch_client = TwitchClient(twitch_api_key)

    def run(self):
        streamers = self.config['streamers']
        self.logger.debug('{} streamers loaded: {}'.format(
            len(streamers),
            ', '.join(streamers)
            ))

        while True:
            self.poll()

            self.logger.debug('Checking again in {}s'.format(
                self.check_interval))
            time.sleep(self.check_interval)

    # Polls the streamer statuses from the Twitch API.
    def poll(self):
        streamers = self.config['streamers']
        res = self.twitch_client.get_streams({'user_login': streamers.keys(),
                                              'first': 100})
        streams = res.get('data', [])

        for stream in streams:
            username = stream['user_name'].lower()
            options = streamers[username]

            self.logger.debug("{} is live - options: {}".format(
                username, options))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    recorder = TwitchRecorder()
    recorder.load_config('config.toml')
    recorder.run()
