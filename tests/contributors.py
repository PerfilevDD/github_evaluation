from github import GithubException
from tester.tester import Tester
from .test_main import TestResult, retry_result_func

def contributors_check(c: Tester) -> TestResult:
    try:
        # Check of contributors
        contribs = c.client.get_repo(f"{c.owner}/{c.repo}").get_contributors()
    except GithubException as e:
        return retry_result_func(e)
    
    companies = set()
    
    for contrib in contribs:
        if contrib.contributions >= 5:
            try:
                # check client
                user = c.client.get_user(contrib.login)
                company = user.company
                if company:
                    companies.add(company)
            except GithubException as e:
                return retry_result_func(e)

        if len(companies) > 2:
            return TestResult(pass_=True, confidence=10)
    

    return TestResult(pass_=False, confidence=10)

