from tester.tester import Tester
from .test_main import TestResult

def pull_requests(c: Tester, commit_limit=10) -> TestResult:
    try:
        commits = c.client.get_repo(f"{c.owner}/{c.repo}").get_commits()[:commit_limit]
        
        total = 0
        total_with_prs = 0

        for commit in commits:
            committer = commit.committer.login if commit.committer else ""
            is_bot = any(substring in committer for substring in ["bot", "gardener"])
            
            if is_bot:
                continue

            commit_data = c.client.get_repo(f"{c.owner}/{c.repo}").get_commit(commit.sha)
            prs = commit_data.get_pulls()
            
            total += 1
            if prs.totalCount > 0:
                total_with_prs += 1
        
        if total > 0:
            actual_ratio = total_with_prs / total
            pass_threshold = actual_ratio >= 0.75
            confidence = int(actual_ratio * 10)
            return TestResult(pass_=pass_threshold, confidence=confidence)
        else:
            return TestResult(pass_=False, confidence=0)

    except Exception as e:
        print(e)
        return TestResult(pass_=False, confidence=0, error=str(e))
