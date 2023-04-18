#!/usr/bin/env bash
#!/bin/sh
gunicorn -b 0.0.0.0:8000 app:server --timeout 300
