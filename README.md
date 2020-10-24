# jupyslack

Slack integration for notebooks. Keep track of your code right in your pocket.

## Installation :

```console
$ pip install jupyslack
```
## Connection to Slack :
First, you need to create an authorization token on your Slack account.

```python
In [1]: %load_ext jupyslack

In [2]: %jupyslack setup <slack_token> #<channel_name>
"Connected to Slack !"
```

## Turn on cell execution tracking

```python
In [3]: %jupyslack track
```

## Turn off cell execution tracking

```python
In [3]: %jupyslack untrack
```
