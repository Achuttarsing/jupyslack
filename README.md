# jupyslack

Slack integration for notebooks. Keep track of your code right in your pocket.

<img src="https://user-images.githubusercontent.com/24542347/97366361-7bc44f00-18a7-11eb-8450-5a3fcec5f3bf.PNG" alt="drawing" width="200"/><img src="https://user-images.githubusercontent.com/24542347/97365895-ba0d3e80-18a6-11eb-97df-9ae89cbade42.PNG" alt="drawing" width="200"/>


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

## To track a cell, simply put this magic line at its beggining :

```python
In [3]: %jupyslack track
```

#### You can give a name to the cell with : -name

```python
In [4]: %jupyslack track -name <name>
```
