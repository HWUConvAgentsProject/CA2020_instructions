from rasa.nlu.model import Interpreter

utterance = u"can i book a table in paris for two persons"

# loading the model from one directory or zip file
interpreter = Interpreter.load("./models/nlu-20200117-113211.tar.gz")

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)
