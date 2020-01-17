
**By gaining access to the contents of this organization, you agree not to distribute or publish any of the contents found here in any way. The access you have can and will only be used for the purposes of Conversational Agents course.**


# General Info
For your coursework you will use the Alana conversational framework. Alana runs as a service and is accessible through an endpoind `http://52.23.135.246:5000`. 
## Setup 
1. Make sure you have the following installed in your system:
- `anaconda` (https://docs.anaconda.com/anaconda/install/)
- `ngrok` (https://ngrok.com/) This will be needed in order to expose your bot and make it accessible by Alana.
- (optional) `MongoDB` (e.g. from https://www.mongodb.com/download-center/community). Although MongoDB is not needed, most of you will proboably want to keep track of the internal state of your bots which MongoDB will be of great help.

(After lecture has been given)

2. Install all required packages by running `./alana_installation.sh`. This will create the _Alana_ virtual environment on Anaconda, activate it, and install all the packages there. 

## Usage
As noted earlier, Alana is already running and is accessible as a service. Each team will need to create one or more new bots, that will be added to the ensemble and called by Alana (as exlpained in the classroom). 

On each dialogue turn, you will send a **POST** call to Alana to the aforementioned endpoint. At some point during the pipeline Alana will call all the bots specified on the call (including your own). By using `ngrok` you allow your bot to be accessible by Alana. Ngrok will bind an `ip:port` address to a simple URL like `http://example.ngrok.io`.

![](https://i.ibb.co/42bssJC/Untitled-Diagram.png)

You may use any method to send the calls to Alana on each turn (curl, python requests, etc). The data that you will 
need to send are as follows (example):

```python
{'user_id': 'test-user',
 'question': 'Hello there',   # The string representation of the user's utterance'
 'session_id': 'some-session-id',   # A unique id PER DIALOGUE. For clarity, it could be in the format: "<project_number>.UUID4"
 'overrides': {
    'BOT_LIST': [   # List of ALL the bots that should be called this turn. For most cases this list will remain the same throughout your project.
      'evi',  # For default Alana bots (that are already in the enseble) you can use just their name
      {'awesome-bot': 'http://example.ngrok.io'},   # Don't forget to put your own bot in this list! It should be added as a dictionary in order to include the url
      'news_bot_v2',
      'wiki_bot_mongo',
      'persona'
    ],
    'PRIORITY_BOTS': [    # The priority in which the response will be selected amongst the candidates
      'awesome-bot',
      ['news_bot_v2', 'wiki_bot_mongo'],   # Nested list means that these bots share the same priority
      'persona', 
      'evi'
    ]
  }
}
```
The default `BOT_LIST` list that you will have to add your own bot in is:

```python
BOT_LIST:
    "clarification_bot"
    "ontology_bot"
    "aiml_bot"
    "coherence_bot"
    "evi"
    "weather_bot"
    "fact_bot"
    "news_bot_v2"
    "wiki_bot_mongo"
    "profanity_bot"
    "reddit_bot"
```
(Note that you do NOT need to use every bot in the default list for your project. You can pick and choose the ones you need.)

The default `PRIORITY_BOTS` list that you will have to add your own bot in is:

```python
PRIORITY_BOTS:
- profanity_bot
- facts
- weather
- persona
- [news_bot_v2, ontology_bot, reddit_bot]
- wiki_bot_mongo
- evi
```

An example curl call would look like this:
>curl -X POST -H "Content-Type: application/json" -d '{"user_id":"test-user", "question":"Hello there", "session_id":"CLI-sessionId", "overrides": {"BOT_LIST": ["coherence", {"awesome-bot":"http://example.ngrok.io"}, news, wiki, persona], "PRIORITY_BOTS":["awesome-bot",["news", "wiki"], persona, coherence]}}' http://52.23.135.246:5000

Detailed information about what the `BOT_LIST` and `PRIORITY_BOTS` are will be given during the lab session.
# State Object
The state object that every bot in the ensemble will have access to looks like this:

```python
          {
            'session_id': ...,
            'timestamp': ..., 
            'user_id': ..., 
            'last_state': {...}, # same as this object without the 'last_state' or 'session_id' attributes. It is mainly here for a more direct access to it
            'state': {  
                'last_bot': ...,
                'input': {
                    'text': ..., # this will be the old user_utterance
                    'hypotheses': [...] # tokenized asr confidence scores
                },
                'turn_no': ...,
                'nlu': {
                   'annotations': {
                               'intents': {...},
                               'ner': {...},
                               'processed_text': {...},
                               'profanity': {...},
                               'postag': {...},
                               'sentiment': {...},
                               'topics': {...},
                               ...
                                  },
                   'modules':[ a list of the nlu modules that run in the pipeline ],
                   'processed_text': {...}
                },
                'previous_topics': [...], # list of all unique previous topics in the session
                'response': {<bot_name>: <response>},
                'bot_states': {<bot_name>: {bot_attributes: {...}, # This is the dumping attribute, where each bot can put attributes that needs to be stored in the db for whatever reason (i.e. news_ids, into_bot flags, 
                                    etc)
                                            lock_requested: bool}},
                'system_emotion': ... # Not yet fully used 
                                    
            }
```
**Please note that although the user utterance as it comes from the ASR is in `state.input.text`, the utterance AFTER the preprocessing step is in the `state.nlu.processed_text` so you should use that one in most cases as an input to your bots, since the sentence might have been already transformed in the preprocess.**

## Bot input

So the full input of each bot will be:

```python
{
    'current_state': {...}, # state object as described above (please note that the previous state is also an attribute of this)
    'history': [...], # a list of state dictionaries as above. Can be configured to only get the N last items
    'user_attributes': {
                 'user_id': ...,
                 'user_name': "john",
                 'map_attributes': {...}, # dictionary or various user attributes like
                 'last_session': self.session_id
             }
}
```

Each bot then will need to return a dictionary like this:

```python
{
    'result': [...], # a list of posible response candidates
    'bot_name': ...,
    'lock_requested': bool, # Flag to state that a bot is requesting to handle the next turn as well.
    'bot_params': {...} # the "helper attributes" that the bot requests to be saved (will go in the "bot_state" of 
                      the state object
}
```
Once the dialogue manager collects all these bot responses, it will update the state with the information from the bot that got selected by the ranking function / policy.

Remember that no bot will have access directly to the database, so any information (i.e. turn number that something happened, flags, etc) that a bot needs to retain for the following turns can be saved in that bot's `bot_params`.

# Examples

## State representation

An example output of 2 consequent turns would look like this: 
**NOTE: As of 2019 this might be slightly different**

```python
{u'current_state': {u'last_state': {},
                    u'session_id': u'CLI-00015',
                    u'state': {u'bot_states': {},
                               u'input': {u'avg_conf_score': 1.0,
                                          u'raw': [],
                                          u'text': u'How can I get to a coffee shop'},
                               u'last_bot': None,
                               u'nlu': {u'annotations': {u'intents': {u'intent': u'task_route_descr',
                                                                      u'param': u'a coffee shop'},
                                                         u'ner': {},
                                                         u'postag': [u'coffee shop'],
                                                         u'processed_text': u'How can I get to a coffee shop',
                                                         u'profanity': {u'overallClass': 0,
                                                                        u'text': u'how can i get to a coffee shop',
                                                                        u'values': [{u'confidence': u'1',
                                                                                     u'offensivenessClass': 0,
                                                                                     u'source': u'blacklist'},
                                                                                    {u'confidence': u'0.237502',
                                                                                     u'offensivenessClass': 0,
                                                                                     u'source': u'statistical_model'}]},
                                                         u'sentiment': {u'compound': 0.0,
                                                                        u'neg': 0.0,
                                                                        u'neu': 1.0,
                                                                        u'pos': 0.0},
                                                         u'topics': {u'confidence': 999.0,
                                                                     u'text': u'how can i get to a coffee shop',
                                                                     u'topicClass': u'Music'}},
                                        u'modules': {u'intents': [u'RegexIntents'],
                                                     u'ner': [u'StanfordNER'],
                                                     u'postag': [u'POSTagExtract'],
                                                     u'processed_text': [u'Preprocessor'],
                                                     u'profanity': [u'AmazonProfanityDetector'],
                                                     u'sentiment': [u'VaderNLTK'],
                                                     u'topics': [u'AmazonTopicRecogniser']},
                                        u'processed_text': u'How can I get to a coffee shop'},
                               u'previous_topics': [],
                               u'response': None,
                               u'turn_no': u'1'},
                    u'timestamp': u'2018-04-25T12:53:39Z',
                    u'user_id': u'dummy-user'},
 u'history': [],
 u'user_attributes': {}}




{u'current_state': {u'last_state': {u'state': {u'bot_states': {u'task_bot': {u'bot_attributes': {u'action_name': u'task_route_descr',
                                                                                                 u'params': None,
                                                                                                 u'status': None},
                                                                             u'lock_requested': None}},
                                               u'input': {u'avg_conf_score': 1.0,
                                                          u'raw': [],
                                                          u'text': u'How can I get to a coffee shop'},
                                               u'last_bot': None,
                                               u'nlu': {u'annotations': {u'intents': {u'intent': u'task_route_descr',
                                                                                      u'param': u'a coffee shop'},
                                                                         u'ner': {},
                                                                         u'postag': [u'coffee shop'],
                                                                         u'processed_text': u'How can I get to a coffee shop',
                                                                         u'profanity': {u'overallClass': 0.0,
                                                                                        u'text': u'how can i get to a coffee shop',
                                                                                        u'values': [{u'confidence': u'1',
                                                                                                     u'offensivenessClass': 0.0,
                                                                                                     u'source': u'blacklist'},
                                                                                                    {u'confidence': u'0.237502',
                                                                                                     u'offensivenessClass': 0.0,
                                                                                                     u'source': u'statistical_model'}]},
                                                                         u'sentiment': {u'compound': 0.0,
                                                                                        u'neg': 0.0,
                                                                                        u'neu': 1.0,
                                                                                        u'pos': 0.0},
                                                                         u'topics': {u'confidence': 999.0,
                                                                                     u'text': u'how can i get to a coffee shop',
                                                                                     u'topicClass': u'Music'}},
                                                        u'modules': {u'intents': [u'RegexIntents'],
                                                                     u'ner': [u'StanfordNER'],
                                                                     u'postag': [u'POSTagExtract'],
                                                                     u'processed_text': [u'Preprocessor'],
                                                                     u'profanity': [u'AmazonProfanityDetector'],
                                                                     u'sentiment': [u'VaderNLTK'],
                                                                     u'topics': [u'AmazonTopicRecogniser']},
                                                        u'processed_text': u'How can I get to a coffee shop'},
                                               u'previous_topics': [],
                                               u'response': {u'task_bot': u'You mean Costa or Starbucks'},
                                               u'turn_no': u'1'},
                                    u'timestamp': u'2018-04-25T12:53:39Z',
                                    u'user_id': u'dummy-user'},
                    u'session_id': u'CLI-00015',
                    u'state': {u'bot_states': {u'task_bot': {u'bot_attributes': {u'action_name': u'task_route_descr',
                                                                                 u'params': None,
                                                                                 u'status': None},
                                                             u'lock_requested': None}},
                               u'input': {u'avg_conf_score': 1.0,
                                          u'raw': [],
                                          u'text': u'Costa'},
                               u'last_bot': u'task_bot',
                               u'nlu': {u'annotations': {u'intents': {u'intent': u'task_route_descr',
                                                                      u'param': u'<cmd>{"action":"task_route_descr"'},
                                                         u'ner': {u'LOCATION': [u'costa'],
                                                                  u'ORGANIZATION': [u'starbucks']},
                                                         u'postag': [u'Costa'],
                                                         u'processed_text': u'Costa',
                                                         u'profanity': {u'overallClass': 0,
                                                                        u'text': u'Costa',
                                                                        u'values': [{u'confidence': u'1',
                                                                                     u'offensivenessClass': 0,
                                                                                     u'source': u'blacklist'},
                                                                                    {u'confidence': u'0.403462',
                                                                                     u'offensivenessClass': 0,
                                                                                     u'source': u'statistical_model'}]},
                                                         u'sentiment': {u'compound': 0.0,
                                                                        u'neg': 0.0,
                                                                        u'neu': 1.0,
                                                                        u'pos': 0.0},
                                                         u'topics': {u'confidence': 0.521,
                                                                     u'text': u'<removed_for_example>'}},
                                        u'modules': {u'intents': [u'RegexIntents'],
                                                     u'ner': [u'StanfordNER'],
                                                     u'postag': [u'POSTagExtract'],
                                                     u'processed_text': [u'Preprocessor'],
                                                     u'profanity': [u'AmazonProfanityDetector'],
                                                     u'sentiment': [u'VaderNLTK'],
                                                     u'topics': [u'AmazonTopicRecogniser']},
                                        u'processed_text': u'Costa'},
                               u'previous_topics': [],
                               u'response': None,
                               u'turn_no': u'2'},
                    u'timestamp': u'2018-04-25T12:53:39Z',
                    u'user_id': u'dummy-user'},
 u'history': [{u'state': {u'bot_states': {u'task_bot': {u'bot_attributes': {u'action_name': u'task_route_descr',
                                                                            u'params': None,
                                                                            u'status': None},
                                                        u'lock_requested': None}},
                          u'input': {u'avg_conf_score': 1.0,
                                     u'raw': [],
                                     u'text': u'How can I get to a coffee shop'},
                          u'last_bot': None,
                          u'nlu': {u'annotations': {u'intents': {u'intent': u'task_route_descr',
                                                                 u'param': u'a coffee shop'},
                                                    u'ner': {},
                                                    u'postag': [u'coffee shop'],
                                                    u'processed_text': u'How can I get to a coffee shop',
                                                    u'profanity': {u'overallClass': 0.0,
                                                                   u'text': u'how can i get to a coffee shop',
                                                                   u'values': [{u'confidence': u'1',
                                                                                u'offensivenessClass': 0.0,
                                                                                u'source': u'blacklist'},
                                                                               {u'confidence': u'0.237502',
                                                                                u'offensivenessClass': 0.0,
                                                                                u'source': u'statistical_model'}]},
                                                    u'sentiment': {u'compound': 0.0,
                                                                   u'neg': 0.0,
                                                                   u'neu': 1.0,
                                                                   u'pos': 0.0},
                                                    u'topics': {u'confidence': 999.0,
                                                                u'text': u'how can i get to a coffee shop',
                                                                u'topicClass': u'Music'}},
                                   u'modules': {u'intents': [u'RegexIntents'],
                                                u'ner': [u'StanfordNER'],
                                                u'postag': [u'POSTagExtract'],
                                                u'processed_text': [u'Preprocessor'],
                                                u'profanity': [u'AmazonProfanityDetector'],
                                                u'sentiment': [u'VaderNLTK'],
                                                u'topics': [u'AmazonTopicRecogniser']},
                                   u'processed_text': u'How can I get to a coffee shop'},
                          u'previous_topics': [],
                          u'response': {u'task_bot': u'You mean Costa or Starbucks'},
                          u'turn_no': u'1'},
               u'timestamp': u'2018-04-25T12:53:39Z',
               u'user_id': u'dummy-user'}],
 u'user_attributes': {}}
```

## Advanced NLU pipeline response

Given the user utterance `hello how are you`, the NLU pipeline will return the following JSON response

```
{
    "session_id": "CLI-a761a305-122f-4b56-993a-882f3b3aefdb",
    "timestamp": "2019-01-18T15:11:44Z",
    "user_id": "1117",
    "last_state": {},
    "state": {
        "last_bot": null,
        "input": {
            "text": "hello how are you",
            "hypotheses": null
        },
        "turn_no": "1",
        "nlu": {
            "annotations": {
                "processed_text": "Hello how are you",
                "sentiment": {
                    "neg": 0.0,
                    "neu": 1.0,
                    "pos": 0.0,
                    "compound": 0.0
                },
                "intents": {
                    "intent": null,
                    "param": null,
                    "all": []
                },
                "postag": [
                    [
                        "Hello",
                        "NNP"
                    ],
                    [
                        "how",
                        "WRB"
                    ],
                    [
                        "are",
                        "VBP"
                    ],
                    [
                        "you",
                        "PRP"
                    ]
                ],
                "nps": [
                    "Hello"
                ]
            },
            "modules": {
                "processed_text": [
                    "Preprocessor",
                    "Truecaser",
                    "TellMeAboutNormaliser"
                ],
                "sentiment": [
                    "VaderNLTK"
                ],
                "intents": [
                    "RegexIntents",
                    "PersonaRegexTopicClassifier"
                ],
                "postag": [
                    "MorphoTagger"
                ],
                "nps": [
                    "NPDetector"
                ]
            },
            "processed_text": "Hello how are you"
        },
        "previous_topics": [],
        "response": {
            "evi": "Hmmm... I'm feeling super productive. I've set a gazillion timers, and now I'm brushing up on my Klingon."
        },
        "response_edits": null,
        "bot_states": {
            "evi": {
                "lock_requested": null,
                "bot_attributes": {}
            }
        },
        "system_emotion": null
    }
}ull
    }
}
```

# Bot usage

In order to generate a new bot, you will need to install the `utils` library, which contains some useful custom objects for each bot. It should be installed automatically during the system initial installation..
Most importantly you will need the `sample_bot` template to start constructing your bot. This is a simple 
example bot that shows how the state object can be used.

Using this template also means that you will have access to the `response` object to keep in mind what you are expected to return to the Hub. These are the `result`, `bot_name`, `locked_requested` and `bot_params`.