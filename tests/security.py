from tester.tester import Tester
from .test_main import TestResult

def security_md_check(c: Tester) -> TestResult:
    for file_path in [".github/SECURITY.md", ".github/security.md", "security.md", "SECURITY.md"]:
        try:
            content_file = c.client.get_repo(f"{c.owner}/{c.repo}").get_contents(file_path)
            content_file.decoded_content  
            return TestResult(pass_=True, confidence=10)
        except Exception:
            continue
    
    return TestResult(pass_=False, confidence=10)

