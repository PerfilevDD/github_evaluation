from tester.tester import Tester
from .test_main import TestResult

def signed_tags(c: Tester) -> TestResult:
    try:
        tags = c.client.get_repo(f"{c.owner}/{c.repo}").get_tags()
        
        total_releases = 0
        total_signed = 0

        for tag in tags:
            total_releases += 1
            commit_sha = tag.commit.sha
            commit = c.client.get_commit(f"{c.owner}/{c.repo}", commit_sha)
            if commit.commit.verification.verified:
                total_signed += 1

        # Threshold is 3/4 of releases
        actual = total_signed / total_releases if total_releases > 0 else 0
        if actual >= 0.75:
            return TestResult(pass_=True, confidence=int(actual * 10))
        
        return TestResult(pass_=False, confidence=int(10 - actual * 10))

    except Exception as e:
        return TestResult(pass_=False, confidence=5, error=str(e))

