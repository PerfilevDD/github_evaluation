from tester.tester import Tester
import os
tester_instance = Tester(owner="github", repo="docs", token=os.getenv("GITHUB_AUTH_TOKEN"))
repo = tester_instance.get_repository()
print(repo.full_name)



from tests.active import is_active
result_active= is_active(tester_instance)
print(f"active: {result_active.pass_}, Confidence: {result_active.confidence}")

from tests.contributors import contributors_check

from tester.tester import Tester
from tests.releases import signed_releases
from tests.security import security_md_check



from tests.pull_requests import pull_requests
result_pull_requests = pull_requests(tester_instance)
print(f"pull_requests: {result_pull_requests.pass_}, Confidence: {result_pull_requests.confidence}")





result_contributors = contributors_check(tester_instance)
print(f"contributors: {result_contributors.pass_}, Confidence: {result_contributors.confidence}")

result_security = security_md_check(tester_instance)
print(f"security: {result_security.pass_}, Confidence: {result_security.confidence}")

result_releases = signed_releases(tester_instance)
print(f"releases: {result_releases.pass_}, Confidence: {result_releases.confidence}")




score = result_pull_requests.confidence + result_active.confidence + result_contributors.confidence + result_security.confidence + result_releases.confidence
print(f"score {round((score/5), 2)}")




from session_helper.session_helper import new_github_session
session = new_github_session()
response = session.get("https://api.github.com/repos/github/docs/contributors")
print(response.json())
