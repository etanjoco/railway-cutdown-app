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

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- To learn about Hypercorn and how to configure it, read their [Documentation](https://hypercorn.readthedocs.io/)
