# RASA Tutorial

In this tutorial we will learn how to create a chatbot that is able to support a conversation about
restaurant booking. The task has been defined in the literature in the paper [Learning End-to-End Goal-Oriented Dialog
](https://arxiv.org/abs/1605.07683). The full dataset 
can be downloaded from [official website](https://research.fb.com/downloads/babi/). In this practical session will briefly recap how to build NLU systems using RASA and we will integrate the NLU component in a working chatbot able to do restaurant recommendation.

## Setup 

First of all, make sure that you have Anaconda installed on your system. Check the Lab2 tutorial sheet for more instructions. Once you've correctly installed the framework, activate the `Alana`:

```
conda activate Alana
```

Now we are going to install RASA. Please run the command `pip install rasa`. 

To make sure that the installation process is successfully completed, run the command `rasa` from your terminal. You should be getting an output that looks like the following one:

```
usage: rasa [-h] [--version]
            {init,run,shell,train,interactive,test,visualize,data,x} ...

Rasa command line interface. Rasa allows you to build your own conversational
assistants 🤖. The 'rasa' command allows you to easily run most common commands
like creating a new bot, training or evaluating models.

positional arguments:
  {init,run,shell,train,interactive,test,visualize,data,x}
                        Rasa commands
    init                Creates a new project, with example training data,
                        actions, and config files.
    run                 Starts a Rasa server with your trained model.
    shell               Loads your trained model and lets you talk to your
                        assistant on the command line.
    train               Trains a Rasa model using your NLU data and stories.
    interactive         Starts an interactive learning session to create new
                        training data for a Rasa model by chatting.
    test                Tests Rasa models using your test NLU data and
                        stories.
    visualize           Visualize stories.
    data                Utils for the Rasa training files.

optional arguments:
  -h, --help            show this help message and exit
  --version             Print installed Rasa version
  ```
