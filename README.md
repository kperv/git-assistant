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
* 50 git related questions and answers (ChatGPT 4o-mini generated)
* cosine similarity

## Steps to reproduce

set up llama3 in ollama

run script for in-browser view
``` bash
./run.sh
```

## Deployment to the Cloud

The project is deployed on a remote machine with 2 GPUs.
Port 80 is used to map Streamlit app to domain git-assistant.pro
