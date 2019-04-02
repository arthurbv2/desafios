import os
from collections import defaultdict


class Configurations:

    def __init__(self):
        self.config = defaultdict(dict)
        self.config['telegram_bot_token'] = os.environ['TELEGRAM_BOT_TOKEN']
