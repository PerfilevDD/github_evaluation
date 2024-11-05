import tester.active
import tester.contributors
import tester.pull_requests
import tester.releases
import tester.security
import tester.tags
from .test_main import all_tests, NamedCheck

def import_all():
    all_tests.append(NamedCheck(name="Active", fn=tester.active.is_active))
    all_tests.append(NamedCheck(name="Contributors", fn=tester.contributors.contributors_check))
    all_tests.append(NamedCheck(name="Pull-Requests", fn=tester.pull_requests.pull_requests))
    all_tests.append(NamedCheck(name="Signed-Releases", fn=tester.releases.signed_releases))
    all_tests.append(NamedCheck(name="Security-MD", fn=tester.security.security_md_check))