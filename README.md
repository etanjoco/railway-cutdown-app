---
title: FastAPI
description: A FastAPI server
tags:
  - fastapi
  - hypercorn
  - python
---

# FastAPI Example

This example starts up a [FastAPI](https://fastapi.tiangolo.com/) server.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-NvLj4?referralCode=CRJ8FE)
## ✨ Features

- FastAPI
- [Hypercorn](https://hypercorn.readthedocs.io/)
- Python 3

## 💁‍♀️ How to use

- Clone locally and install packages with pip using `pip install -r requirements.txt`
- Run locally using `hypercorn main:app --reload`

## 🚀 Docker

Run with Docker Compose:

```bash
docker compose up --build
```

Or run detached:

```bash
docker compose up -d --build
```

Stop the service:

```bash
docker compose down
```

The app will be available at http://localhost:8000/

## 🖥️ Web UI

A simple web interface is available at the root URL. It fetches the player list from `/players` and displays it in a table.

Open in your browser after starting the server:

```bash
http://localhost:8000/
```

## 📥 Import players from CSV

You can import players using the `/players/import` endpoint which accepts a multipart form with a file field named `file`.

Requirements:
- CSV must include a header row with the columns: `name`, `grade`.
- The import upserts by `name`+`grade` (existing rows with the same `name` and `grade` will be updated).
- The import is best-effort: valid rows are inserted/updated and invalid rows are skipped; a summary is returned.

Example using `curl`:

```bash
curl -F "file=@players.csv" http://localhost:8000/players/import
```

Response format:

```json
{"processed":N,"inserted":I,"updated":U,"skipped":S,"errors":[...]} 
```

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- To learn about Hypercorn and how to configure it, read their [Documentation](https://hypercorn.readthedocs.io/)
