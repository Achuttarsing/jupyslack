from IPython.core.magic import register_line_magic
import requests
import json
import re

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
                "text": "I'm now connected to your notebook ! I good do plenty of things like :"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• Keep you in track \n• Manage and update attendees \n• Get notified about changes of your meetings"
            }
        }
    ]



class slackInstance():
    def __init__(self):
        self.slack_token = None
        self.slack_channel = None
        self.ipython_version = IPython.version_info[0]

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

    def notify_end_execution(self, results):
        self.post_message_to_slack('Execution ended')
        IPython.get_ipython().events.unregister('post_run_cell', notify_end_execution)

    def notify_end_execution_colab(self):
        self.post_message_to_slack('Execution ended')
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
        command = args.split(" ")
        if command[0] == 'setup':
            if len(command) != 3:
                print("Please retry with : jupyslack setup <slack_token> #<channel_name>")
            else:
                # regex to accept both "token", 'token' and token
                tok_str, chan_str = re.sub('^[\'|\"]','',command[1]), re.sub('^[\'|\"]','',command[2])
                tok_str, chan_str = re.sub('[\'|\"]$','',tok_str), re.sub('[\'|\"]$','',chan_str)
                inst.slack_token, inst.slack_channel = tok_str, chan_str
                inst.check_setup()
        elif command[0] == 'track':
            ipython.events.register('post_run_cell', notify_end_execution)







