import requests
import json

BEARER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyMjA4MDEwOThAcmFqYWxha3NobWkuZWR1LmluIiwiZXhwIjoxNzUxNjk0MzQ1LCJpYXQiOjE3NTE2OTM0NDUsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiJlZGE5ZWQwNy0wOWFmLTQwMmYtYTBiNS1lMjZkZGI3MTNlNWEiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJrYXJ0aGlrZXlhbiBhIiwic3ViIjoiNDIwYjU4ZTUtNmYwYy00NjgzLThjN2QtY2NmZjIxODk3ZTRhIn0sImVtYWlsIjoiMjIwODAxMDk4QHJhamFsYWtzaG1pLmVkdS5pbiIsIm5hbWUiOiJrYXJ0aGlrZXlhbiBhIiwicm9sbE5vIjoiMjIwODAxMDk4IiwiYWNjZXNzQ29kZSI6ImNXeWFYVyIsImNsaWVudElEIjoiNDIwYjU4ZTUtNmYwYy00NjgzLThjN2QtY2NmZjIxODk3ZTRhIiwiY2xpZW50U2VjcmV0IjoieHhWUXBja1BFc3JheXdrUyJ9.grfkt880o-T1kuu7WtnfMhdSKFW9TolR8WDmk1ypY5s'

def Log(stack: str, level: str, package: str, message: str):
    log_url = "http://20.244.56.144/evaluation-service/logs"

    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }

    body = {
        "stack": "backend",
        "level": level,
        "package": package,
        "message": message
    }

    try:
        response = requests.post(log_url, headers=headers, json=body)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status() 
        
        print(f"Log sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log: {e}")