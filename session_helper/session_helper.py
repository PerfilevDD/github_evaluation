import os
import time
import logging
from requests import Session, Request, Response
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from threading import Lock

GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")

class GitHubAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

class RateLimitAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        response = super().send(request, **kwargs)
        remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
        
        if remaining <= 0:
            reset = int(response.headers.get("X-RateLimit-Reset", 0))
            wait_time = max(0, reset - int(time.time()))
            logging.info(f"Rate limit exceeded. Waiting {wait_time} seconds to retry...")
            time.sleep(wait_time)
            return super().send(request, **kwargs)
        
        return response

class CachingSession(Session):
    def __init__(self):
        super().__init__()
        self.resp_cache = {}
        self.body_cache = {}
        self.lock = Lock()

    def request(self, method, url, *args, **kwargs):
        parsed_url = urlparse(url)

        with self.lock:
            if parsed_url in self.resp_cache:
                logging.info(f"Cache hit on {url}")
                cached_response = self.resp_cache[parsed_url]
                cached_response._content = self.body_cache[parsed_url]
                return cached_response

        response = super().request(method, url, *args, **kwargs)
        
        if response.status_code == 200:
            with self.lock:
                self.resp_cache[parsed_url] = response
                self.body_cache[parsed_url] = response.content
        
        return response

def new_github_session():
    token = os.getenv(GITHUB_AUTH_TOKEN)
    session = CachingSession()
    
    if token:
        session.auth = GitHubAuth(token)

    rate_limit_adapter = RateLimitAdapter()
    session.mount("https://", rate_limit_adapter)
    return session
