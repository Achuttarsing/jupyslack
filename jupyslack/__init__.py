from IPython.core.magic import register_line_magic
import requests
import json
import re
import time
import shlex

start_block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hi there :wave:"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "I'm now connected to your notebook ! \n\nNow you can track a cell by adding *%jupyslack track* at its begginning. And you can add the following arguments :"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• *-name* : to specify a name to the cell"
            }
        }
    ]

class slackInstance():
    def __init__(self):
        self.slack_token = None
        self.slack_channel = None
        self.ipython_version = IPython.version_info[0]
        self.starttime = None
        self.name = None

    def post_message_to_slack(self, text, blocks = None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': self.slack_token,
            'channel': self.slack_channel,
            'text': text,
            'icon_url': 'https://freeiconshop.com/wp-content/uploads/edd/earth-flat.png',
            'username': 'Jupyslack',
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    def check_setup(self):
        res = self.post_message_to_slack('Connected to Slack !', blocks=start_block)
        if res['ok'] is True:
            print("Connected to Slack !")
        else:
            print("Error :",res['error'])

    def before_execution(self, name=None):
        self.starttime = time.time()
        if name is not None : self.name = name

    def notify_end_execution(self, results):
        runtime = time.time() - self.starttime
        if self.name is not None:
            self.post_message_to_slack(self.name+' Execution ended in '+str(runtime)+" sec")
        else:
            self.post_message_to_slack('Execution ended in '+str(runtime)+" sec")
        self.starttime = None
        self.name = None
        IPython.get_ipython().events.unregister('post_run_cell', notify_end_execution)

    def notify_end_execution_colab(self):
        runtime = time.time() - self.starttime
        if self.name is not None:
            self.post_message_to_slack(self.name+' Execution ended in '+str(runtime)+" sec")
        else:
            self.post_message_to_slack('Execution ended in '+str(runtime)+" sec")
        self.starttime = None
        self.name = None
        IPython.get_ipython().events.unregister('post_run_cell', notify_end_execution)


import IPython

ip = IPython.get_ipython()
inst = slackInstance()

if inst.ipython_version > 5:
    notify_end_execution = inst.notify_end_execution
else:
    notify_end_execution = inst.notify_end_execution_colab


def load_ipython_extension(ipython):

    @register_line_magic("jupyslack")
    def lmagic(args):
        command = shlex.split(args)
        if command[0] == 'setup':
            if len(command) != 3:
                print("Please retry with : jupyslack setup <slack_token> #<channel_name>")
            else:
                inst.slack_token, inst.slack_channel = command[1], command[2]
                inst.check_setup()
        elif command[0] == 'track':
            name = command[command.index("-name")+1] if "-name" in command else None
            inst.before_execution(name=name)
            ipython.events.register('post_run_cell', notify_end_execution)







