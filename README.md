# git-assistant

AI model to answer questions about Git.

The book Pro Git is used to provide additional knowledge to a model. [Pro Git](https://git-scm.com/book/en/v2)

The project is **live** on [git-assistant.pro](http://git-assistant.pro/)

## What git-assistant can do?

When working with Git there could be different questions:

- What is git?

- How can I add my files?

- How to revert changes?


Let Git Assistant answer them in short and useful way. 


## Technologies

* LLM: LLama3
* Knowledge base: Elasticsearch (with Hybrid Search Text + Vector)
* Interface: Streamlit

## Evaluation

### Offline evaluation
A dataset with 50 git related questions and answers was generated for evaluation.
Model `gpt-4o-mini` was used for judging and generating ground truth data.

Evaluation is performed by
* cosine similarity is 46%
* LLM-as-a-judge method
RELEVANT           31
PARTLY_RELEVANT    11
NON_RELEVANT       11

## Steps to reproduce

### application

set up llama3 in ollama

then run bash script
``` bash
./run.sh
```
The application will be on 80 port.

### evaluation

``` bash
python eval.py
python eval_with_llm.py
```

## Deployment to the Cloud

The project is deployed on a remote machine with 2 GPUs.
Port 80 is used to map Streamlit app to domain git-assistant.pro
