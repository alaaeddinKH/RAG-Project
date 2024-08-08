# Mini RAG app
This is a minmal implementation of the RAG model for quastion and answer

## Requirements:

- Python 3.8 or later

- Install miniconda

- Create new env by this command:
```bash
$ conda create -n (env-name) python=3.8
```
- activate the env by this command
```bash
$ conda activate (env-name)
```
### Optional

setup your command line to better readablity
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation:

### install the reguirements packages
```bash
$ pip install -r requirements.txt
```

### Setup the environments vairables:
```bash
$ cp .env.example .env
```
Then set the environment vairables in the .env file.

## Run the FastAPI server by
```bash
$ uvicorn main:app --reload
```

