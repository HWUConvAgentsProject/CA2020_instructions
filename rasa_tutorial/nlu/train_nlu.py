from rasa.nlu.model import Trainer
from rasa.nlu import config
from rasa.nlu.training_data import load_data

# loading training data
training_data = load_data('./data/nlu.md')

# initialising the trainer
trainer = Trainer(config.load("config.yml"))

# training
trainer.train(training_data)

# saving the model in the specified directory
trainer.persist('./models/')
