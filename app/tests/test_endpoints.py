from fastapi import FastAPI
from fastapi.testclient import TestClient

# Your current app setup
from app.main import app

client = TestClient(app)

# List all routes
from fastapi.routing import APIRoute

for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"{route.path}")