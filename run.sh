#!/bin/bash

docker compose build && docker compose up && streamlit run app.py --server.port 80