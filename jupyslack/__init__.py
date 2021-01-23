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
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Otherwise, for the lazy ones, you can activate the automatic tracking with *%jupyslack autotrack*. This will notify you for all cells whose runtime is above a certain threshold :"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• *-mintime* : minimum runtime (sec) to send the notification (default=120)"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "And use *%jupyslack untrack* to stop the autotracking"
            }
        }
    ]

class slackInstance():
    def __init__(self):
        self.slack_token = None
        self.slack_channel = None
        self.ipython_version = IPython.version_info[0]
        self.starttime = None
        self.name = "Cell"
        self.autotrack_threshold = None
        self.manual_track = False

    def post_message_to_slack(self, text, blocks = None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': self.slack_token,
            'channel': self.slack_channel,
            'text': text,
            'icon_emoji': ':telescope:',
            'username': 'Jupyslack',
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    def setup_autotrack(self, autotrack_threshold=120):
        self.autotrack_threshold = autotrack_threshold
        print('(jupyslack) autotrack activated for all',str(self.autotrack_threshold)+"+ sec execution cells")

    def check_setup(self):
        res = self.post_message_to_slack('Connected to Slack !', blocks=start_block)
        if res['ok'] is True:
            print("(jupyslack) Connected to Slack !")
        else:
            print("(jupyslack) Error :",res['error'])

    def before_execution(self, name=None):
        self.starttime = time.time()
        self.manual_track = True
        if name is not None : self.name = name

    def pre_before_execution(self, info, name=None):
        self.starttime = time.time()
        if name is not None : self.name = name

    def pre_before_execution_colab(self, name=None):
        self.starttime = time.time()
        if name is not None : self.name = name

    def notify_end_execution(self, results):
        if self.starttime != None:
            success_status = ":white_check_mark: " if ip.last_execution_succeeded == True else ":x: "
            self.post_message_to_slack(success_status+self.name+' execution ended', blocks=self.build_block_end_execution())
        self.starttime = None
        self.name = "Cell"
        IPython.get_ipython().events.unregister('post_run_cell', notify_end_execution)

    def notify_end_execution_colab(self):
        if self.starttime != None:
            success_status = ":white_check_mark: " if ip.last_execution_succeeded == True else ":x: "
            self.post_message_to_slack(success_status+self.name+' execution ended', blocks=self.build_block_end_execution())
        self.starttime = None
        self.name = "Cell"
        IPython.get_ipython().events.unregister('post_run_cell', notify_end_execution)

    def post_notify_end_execution_autotrack(self, results):
        if (self.starttime != None) and (time.time() - self.starttime) > self.autotrack_threshold and self.manual_track == False:
            success_status = ":white_check_mark: " if ip.last_execution_succeeded == True else ":x: "
            self.post_message_to_slack(success_status+self.name+' execution ended', blocks=self.build_block_end_execution())
        self.manual_track = False

    def post_notify_end_execution_autotrack_colab(self):
        if (self.starttime != None) and (time.time() - self.starttime) > self.autotrack_threshold and self.manual_track == False:
            success_status = ":white_check_mark: " if ip.last_execution_succeeded == True else ":x: "
            self.post_message_to_slack(success_status+self.name+' execution ended', blocks=self.build_block_end_execution())
        self.manual_track = False

    def build_block_end_execution(self):
        endtime = time.time()
        runtime = round(endtime - self.starttime)
        if ip.last_execution_succeeded == True:
            text_header = ":white_check_mark: Successful execution ! "
            text_main = "*"+self.name+"* execution has just ended with success !\n\n*Start time:* "+time.strftime('%d-%b %H:%M:%S', time.localtime(self.starttime))+"\n*End time:* "+time.strftime('%d-%b %H:%M:%S', time.localtime(endtime))+"\n*Execution time:* "+time.strftime('%H:%M:%S', time.gmtime(runtime))
        else:
            text_header = ":x: Execution error ! "
            text_main = "*"+self.name+"* execution encountered an error :\n\n`"+ip.get_exception_only()[:-2]+"`\n\n*Start time:* "+time.strftime('%d-%b %H:%M:%S', time.localtime(self.starttime))+"\n*End time:* "+time.strftime('%d-%b %H:%M:%S', time.localtime(endtime))+"\n*Execution time:* "+time.strftime('%H:%M:%S', time.gmtime(runtime))
        block = [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": text_header,
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text_main
                }
            }
        ]
        return block


import IPython

ip = IPython.get_ipython()
inst = slackInstance()

if inst.ipython_version > 5:
    notify_end_execution = inst.notify_end_execution
    pre_before_execution = inst.pre_before_execution
    post_notify_end_execution_autotrack = inst.post_notify_end_execution_autotrack
else:
    notify_end_execution = inst.notify_end_execution_colab
    pre_before_execution = inst.pre_before_execution_colab
    post_notify_end_execution_autotrack = inst.post_notify_end_execution_autotrack_colab


def load_ipython_extension(ipython):

    @register_line_magic("jupyslack")
    def lmagic(args):
        command = shlex.split(args)
        if command[0] == 'setup':
            if len(command) != 3:
                print("(jupyslack) Please retry with : jupyslack setup <slack_token> #<channel_name>")
            else:
                inst.slack_channel = command[2] if command[2][0] == '#' else '#'+command[2]
                inst.slack_token = globals()[command[1][1:]] if command[1][0] == '$' else command[1]
                inst.check_setup()
        elif command[0] == 'track':
            name = command[command.index("-name")+1] if "-name" in command else None
            inst.before_execution(name=name)
            ipython.events.register('post_run_cell', notify_end_execution)
        elif command[0] == 'autotrack':
            min_time = int(command[command.index("-mintime")+1]) if "-mintime" in command else 120
            inst.setup_autotrack(autotrack_threshold=min_time)
            ipython.events.register('pre_run_cell', pre_before_execution)
            ipython.events.register('post_run_cell', post_notify_end_execution_autotrack)
        elif command[0] == 'untrack':
            try:
                ipython.events.unregister('pre_run_cell', pre_before_execution)
                ipython.events.unregister('post_run_cell', post_notify_end_execution_autotrack)
            except:
                pass


