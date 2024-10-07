# git-assistant
AI assistant to help with git version control
The project is live on **git-assistant.pro**

## What git-assistant can do?


What is git?

How can I add my files?

How to revert changes?


There is a book Pro Git (https://git-scm.com/book/en/v2) that has all the answers. There is no need to read it, let Git Assistant read it for you and answer them in short and useful way. 


## Technologies

* LLM LLama3 (2 GPUs speed up)
* Knowledge base: Elasticsearch
* Monitoring: Grafana (in development - dev branch)
* Interface: Streamlit (Live right now on git-assistant.pro)

## Steps to reproduce

set up llama3 in ollama

run script for in-browser view
``` bash
./run.sh
```
