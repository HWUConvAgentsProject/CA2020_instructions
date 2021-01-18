
# Week 2 Lab Instructions

0. Read the general instructions and setup info at https://github.com/HWUConvAgentsProject/CA2020_instructions/blob/master/alana_setup/CA2020_README.md
1. Download and extract *Lab-week2.zip* from Vision on your computer.
2. Assuming you have already registered to Ngrok, go to [https://dashboard.ngrok.com/get-started](https://dashboard.ngrok.com/get-started) and download and unzip the ngrok client for your OS. There is no installation, just an executable, so make sure you save it somewhere you can easily remember.
3. Run the command `./ngrok authtoken xxxxxxxxxxxxxxxxxxxx`as it appears for you on that link from within the folder where you unzipped the ngrok client.
4. Run `./ngrok http 5130` to start the ngrok client and bind `localohost:5130` to an accessible url as shown in the picture. You will need the `http` address.
![](https://i.ibb.co/gVXLCzV/image.png)

	Since ngrok requires to stay alive for the link to work (it will change the url upon restart), it's better to run it on a different tab/terminal window/etc.
	
1. Assuming you already have Anaconda installed and setup (type `conda info` on the terminal to check), run the `alana_installation.sh` script to setup a new conda environment and install the required packages for the sample bot to run.
2. Run `conda activate Alana` to activate the virtual environment on the current terminal. You should see something like `(Alana) ~/CA2020:` as prompt.
3. Run `python bot.py` from withing the *sample_bot* folder. The bot should start listening for incoming connections.
4. On a different terminal/tab, run the command `curl -X POST -H "Content-Type: application/json" -d '{"user_id":"test-5827465823641856215", "question":"hi", "session_id":"CLI-1100002", "projectId": "CA2020", "overrides": {"BOT_LIST": ["coherence_bot", {"greetings":"http://b28c735a.ngrok.io"}], "PRIORITY_BOTS":["greetings", "coherence_bot"]}}' http://52.56.181.83:5000`, replacing `http://b28c735a.ngrok.io` with the http url ngrok generated for you.

	If you should see the json response, you succesfully called Alana and Alana called your sample_bot hosted locally.


# Test call in Python3

```python
import requests

data = {'user_id': 'test-user', 'question': 'Hello there', 'session_id': 'CLI-sessionId', 'projectId': 'CA2020', 'overrides': {'BOT_LIST': ['coherence_bot', 'news_bot_v2', 'wiki_bot_mongo'], 'PRIORITY_BOTS': [['news_bot_v2', 'wiki_bot_mongo'], 'coherence_bot']}}

r= requests.post(url='http://852d4761.ngrok.io', json=data)
r.json()
```



