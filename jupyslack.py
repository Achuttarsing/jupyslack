from IPython.core.magic import register_line_magic
import requests
import json

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

    def post_message_to_slack(self, text, blocks = None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': self.slack_token,
            'channel': self.slack_channel,
            'text': text,
            'icon_url': 'https://i.pinimg.com/originals/38/50/0f/38500f35aa4476ace495347eb9fc2224.png',
            'username': 'Jupyslack Bot',
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    def check_setup(self):
        res = self.post_message_to_slack('Connected to Slack !', blocks=start_block)
        if res['ok'] is True:
            print("Connected to Slack !")
        else:
            print("Error :",res['error'])
        

def load_ipython_extension(ipython):
    inst = slackInstance()

    @register_line_magic("jupyslack")
    def lmagic(arg):
        if arg == 'setup':
            print("Please enter Slack token :")
            inst.slack_token = input()
            print("Please enter Slack channel (#<channel_name>) :")
            inst.slack_channel = input()
            inst.check_setup()