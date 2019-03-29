import logger
import toml

class TwitchRecorder:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.streaming_processes = []
        self.config = config

    def run(self):



if __name__ == '__main__':
    config = toml.load('config.toml')

    recorder = TwitchRecorder()
