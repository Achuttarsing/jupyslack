# jupyslack

Slack integration for notebooks. Keep track of your code right in your pocket.

<img src="https://github.com/Achuttarsing/jupyslack/blob/main/doc/assets/IMG_5411.PNG" alt="drawing" width="200"/><img src="https://github.com/Achuttarsing/jupyslack/blob/main/doc/assets/IMG_5412.PNG" alt="drawing" width="200"/>


## Installation :

```console
$ pip install jupyslack
```
## Connection to Slack :
First, you need to create an authorization token on your Slack account.

```python
In [1]: %load_ext jupyslack

In [2]: %jupyslack setup <slack_token> <channel_name>
"Connected to Slack !"
```

## To track a cell, simply put this magic line at its beggining :

```python
In [3]: %jupyslack track
```

##### You can give a name to the cell with : -name

```python
In [4]: %jupyslack track -name <name>
```

## New feature : automatic tracking
This will notify you for all cells whose runtime is above 2 minutes

```python
In [5]: %jupyslack autotrack
```

##### You can set the minimum runtime with : -mintime (default=120)

```python
In [6]: %jupyslack autotrack -mintime <time_in_sec>
```

##### And stop the automatic tracking with :

```python
In [7]: %jupyslack untrack
```
