from github import Github
import requests

class Tester:
    def __init__(self, owner, repo, token=None):

        self.owner = owner
        self.repo = repo
        self.ctx = None 
        self.http_client = requests.Session()  
        
        self.client = Github(token) if token else Github()

    def get_repository(self):
        # create a link to gitlhub repository
        return self.client.get_repo(f"{self.owner}/{self.repo}")
