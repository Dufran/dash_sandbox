# Dash

Dash is framework to quickly build interactive dashboards.
Main advantages is ability to use data formatting tools like pandas,numpy etc.
This allow you to quickly turn any data to representable infographic and build analytics dashboard as separate services

## Features

- Data connection (api, json, csv, basically anything you can get inside python)
- Many components to handle data representation
- Lightweight Flask server to serve page (For production use gunicorn)
- Allow customization with custom css/js (Simple connection of library like Bootstrap)
- No need for separate JS library to handle graphs (handled by built it Plotly.js)

### Example app tasks

- [x] Create a dashboard app with some statistic data
- [x] Connect external css/js library (bootstrap)
- [x] Create couple of graphs to showcase library features
- [x] Create contained app for easy adding as separate service (docker)

### Dev environment

Simply launch app.py inside python debugger in IDE of your choice
and access

```bash
# Launch app.py
python app.py
# Navigate to app url
http://127.0.0.1:8000/
```

### Container environment

```bash
# Launch docker with nginx and gunicorn
docker compose up -d
# Navigate to app url
http://localhost

```
