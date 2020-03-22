## greet + location/price + cuisine + num people
* greet
   - utter_greet
* make_reservation
   - utter_start
   - utter_ask_cuisine
* inform{"cuisine": "italian"}
   - utter_ask_number        <!-- action that the bot should execute -->
* inform{"number": "two"}
   - utter_ask_location
* inform{"location": "rome"}
   - utter_ask_price
* inform{"price": "moderate"}
   - utter_confirm
   - utter_api_call

## greet + location/price + cuisine + num people
* greet
   - utter_greet
* make_reservation{"location": "rome", "price": "cheap"}  <!-- user utterance, in format intent{entities} -->
   - utter_start
   - utter_ask_cuisine
* inform{"cuisine": "spanish"}
   - utter_ask_number        <!-- action that the bot should execute -->
* inform{"number": "six"}
   - utter_confirm
   - utter_api_call

## greet + num. people/cuisine + location + price
* greet
   - utter_greet
* make_reservation{"number": "six", "cuisine": "french"}  <!-- user utterance, in format intent{entities} -->
   - utter_start
   - utter_ask_location
* inform{"location": "bombay"}
   - utter_ask_price        <!-- action that the bot should execute -->
* inform{"price": "cheap"}
   - utter_confirm
   - utter_api_call

## greet + num. people/cuisine/price + location
* greet
   - utter_greet
* make_reservation{"cuisine": "italian", "number": "six", "price": "cheap"} 
   - utter_start
   - utter_ask_location
* inform{"location": "rome"}
   - utter_ask_price
* inform{"price": "cheap"}
   - utter_confirm
   - utter_api_call