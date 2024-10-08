# git-assistant

AI assistant to help with git version control
The project is **live** on [git-assistant.pro](http://git-assistant.pro/)

## What git-assistant can do?


What is git?

How can I add my files?

How to revert changes?


Let Git Assistant answer them in short and useful way. 


## Technologies

* LLM: LLama3
* Knowledge base: Elasticsearch
* Interface: Streamlit

## Evaluation

### Offline evaluation
a dataset of 50 git related questions and answers generated for evaluation.
gpt-4o-mini was used for judging and generating ground truth data.

Evaluation is performed by
* cosine similarity is 46%
* LLM-as-a-judge method
RELEVANT           31
PARTLY_RELEVANT    11
NON_RELEVANT       11

## Steps to reproduce

### application

set up llama3 in ollama

run script for in-browser view
``` bash
./run.sh
```

### evaluation

``` bash
python eval.py
python eval_with_llm.py
```

## Deployment to the Cloud

The project is deployed on a remote machine with 2 GPUs.
Port 80 is used to map Streamlit app to domain git-assistant.pro
