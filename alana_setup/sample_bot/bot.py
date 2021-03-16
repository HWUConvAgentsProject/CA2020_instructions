import logging
import random
from argparse import ArgumentParser

import os
from flask import Flask, request
from flask_restful import Api
from utils import log
from utils.abstract_classes import Bot
from utils.dict_query import DictQuery
from datetime import datetime
import random

app = Flask(__name__)
api = Api(app)
BOT_NAME = "greetings"

logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument('-p', "--port", type=int, default=5130)
parser.add_argument('-l', '--logfile', type=str, default='logs/' + BOT_NAME + '.log')
parser.add_argument('-cv', '--console-verbosity', default='info', help='Console logging verbosity')
parser.add_argument('-fv', '--file-verbosity', default='debug', help='File logging verbosity')


class GreetingsBot(Bot):
    def __init__(self, **kwargs):
        # Warning: the init method will be called every time before the post() method
        # Don't use it to initialise or load files.
        # We will use kwargs to specify already initialised objects that are required to the bot
        super(GreetingsBot, self).__init__(bot_name=BOT_NAME)
        self.greetings = [
            "Ciao",
            "Hello",
            "Hola"
        ]

    def get(self):
        pass

    def post(self):
        # This method will be executed for every POST request received by the server on the
        # "/" endpoint (see below 'add_resource')

        # We assume that the body of the incoming request is formatted as JSON (i.e., its Content-Type is JSON)
        # We parse the JSON content and we obtain a dictionary object
        request_data = request.get_json(force=True)

        # We wrap the resulting dictionary in a custom object that allows data access via dot-notation
        request_data = DictQuery(request_data)

        # We extract several information from the state
        user_utterance = request_data.get("current_state.state.nlu.annotations.processed_text")
        last_bot = request_data.get("current_state.state.last_bot")

        logger.info("------- Turn info ----------")
        logger.info("User utterance: {}".format(user_utterance))
        logger.info("Last bot: {}".format(last_bot))
        logger.info("---------------------------")

        # the 'result' member is intended as the actual response of the bot
        self.response.result = random.choice(self.greetings)
        # we store in the dictionary 'bot_params' the current time. Remember that this information will be stored
        # in the database only if the bot is selected
        self.response.bot_params["time"] = str(datetime.now())
        
        # Here we instruct the Hub to let this bot handle this turn.
        self.response.lock_requested = True

        # The response generated by the bot is always considered as a list (we allow a bot to generate multiple response
        # objects for the same turn). Here we create a singleton list with the response in JSON format
        return [self.response.toJSON()]


if __name__ == "__main__":
    args = parser.parse_args()
    
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    log.set_logger_params(BOT_NAME, logfile=args.logfile,
                          file_level=args.file_verbosity, console_level=args.console_verbosity)

    api.add_resource(GreetingsBot, "/")

    app.run(host="0.0.0.0", port=args.port)
