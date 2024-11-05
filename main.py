import os
import sys
import logging
import threading
from tester.tester import Tester
from tests.test_main import all_checks
from session_helper.session_helper import new_github_session
from queue import Queue
from urllib.parse import urlparse
from tests.add_all_tests import import_all

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--repo", required=True, help="Repo's URL")
args = parser.parse_args()

# Repository-Information
repo_url = args.repo
repo_url = repo_url.replace("https://", "")
parsed_url = urlparse(repo_url)
host = parsed_url.path
path_parts = parsed_url.path.strip("/").split("/")
if len(path_parts) < 2:
    print("error in rep url")
    sys.exit(1)

host, owner, repo = path_parts[:3]
if host != "github.com":
    print(f"Host only github.com.")
    sys.exit(1)

# create a GitHub-Session 
session = new_github_session()

# create a Tester's instance
c = Tester(
    token=os.getenv("GITHUB_AUTH_TOKEN")
    owner=owner,
    repo=repo,
)

# 
results_queue = Queue()
threads = []

import_func = import_all()

# Execute auch Test
def run_check(check):
    retries_remaining = 3
    while retries_remaining > 0:
        result = check.fn(c)
        if result.should_retry:
            logging.error(result.error)
            retries_remaining -= 1
            continue
        break
    results_queue.put((check.name, result))

# Execute all Tests in different threads
for check in all_checks:
    thread = threading.Thread(target=run_check, args=(check,))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

# results sort
results = []
while not results_queue.empty():
    results.append(results_queue.get())

results.sort(key=lambda x: x[0])

total_score = 0

print("\nRESULTS\n-------")
for name, result in results:
    total_score += result.confidence
    print(name, result.pass_, result.confidence)
print(f"\nscore {round((total_score/5), 2)}")
