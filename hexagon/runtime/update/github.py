import os
from urllib.request import Request


def add_github_access_token(request: Request) -> Request:
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    if token:
        request.add_header("Authorization", f"token {token}")

    return request
