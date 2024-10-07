# git-assistant
AI assistant to help with git version control
The project is live on **git-assistant.pro**

## What git-assistant can do?


What is git?
How can I add my files?
How to revert changes?

All these questions might be asked frequently during working on a project. The AI models as Chat-GPT or LLama can help answer them in a short and useful way. 

* Pro git https://git-scm.com/book/en/v2
There is no need to read the Pro Git book, let Git Assistant read it for you!

## Technologies

* LLM LLama3 (2 GPUs speed up!)
* Knowledge base: Elasticsearch
* Monitoring: Grafana (in development - dev branch)
* Interface: Streamlit (Live right now on git-assistant.pro)

## Steps to reproduce

* preload llama3 on ollama

``` bash
./run.sh
```
