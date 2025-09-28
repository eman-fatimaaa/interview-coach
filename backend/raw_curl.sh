#!/bin/bash
API_KEY="PUT-YOUR-ACTUAL-KEY-HERE"

curl \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $API_KEY" \
  https://generativelanguage.googleapis.com/v1/models
