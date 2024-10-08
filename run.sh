#!/bin/bash

docker compose build && docker compose up -d && streamlit run app.py --server.port 80