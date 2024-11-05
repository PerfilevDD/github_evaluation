import datetime
from tester.tester import Tester
from .test_main import TestResult

lookback_days = 90 # amount of days to check

def is_active(c: Tester) -> TestResult:
    return multi_check(
        periodic_commits,
        periodic_releases
    )(c)
    

def periodic_commits(c: Tester) -> TestResult:
    try:
        commits = c.client.get_repo(f"{c.owner}/{c.repo}").get_commits()
        threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=lookback_days)
        total_commits = 0
        
        for commit in commits:
            commit_full = c.client.get_commit(f"{c.owner}/{c.repo}", commit.sha)
            commit_date = commit_full.commit.author.date
            if commit_date > threshold:
                total_commits += 1
            
        confidence = min(10, max(5, total_commits))  # Confidence grows with commits, max 10
        
        return TestResult(pass_=total_commits >= 2, confidence=confidence)
    
    except Exception as e:
        return TestResult(pass_=False, confidence=7, error=str(e))


def periodic_releases(c: Tester) -> TestResult:
    try:
        releases = c.client.get_repo(f"{c.owner}/{c.repo}").get_releases()
        threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=lookback_days)
        total_releases = 0

        for release in releases:
            release_date = release.created_at
            if release_date > threshold:
                total_releases += 1

        confidence = min(10, max(5, total_releases))  # Confidence grows with commits, max 10
        
        return TestResult(pass_=total_releases > 0, confidence=confidence)
    
    except Exception as e:
        return TestResult(pass_=False, confidence=10, error=str(e))

def multi_check(*checks):
    def run_checks(c: Tester) -> TestResult:
        for check in checks:
            result = check(c)
            if not result.pass_:
                return result
        return TestResult(pass_=True, confidence=min(result.confidence for result in checks))
    return run_checks

