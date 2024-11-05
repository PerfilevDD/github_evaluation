from tester.tester import Tester
from .test_main import TestResult, retry_result_func, inconclusive_result

MAX_RELEASES = 15

def signed_releases(c: Tester) -> TestResult:
    try:
        releases = c.client.get_repo(f"{c.owner}/{c.repo}").get_releases()
    except Exception as e:
        return retry_result_func(e)
    
    total_releases = 0
    total_signed = 0
    
    for i, release in enumerate(releases):
        if i >= MAX_RELEASES: # break if more then 20 releases
            break
        try:
            assets = list(release.get_assets())  # Convert PaginatedList to a list
        except Exception as e:
            return retry_result_func(e)
        
        if len(assets) <= 1:  
            continue
        
        total_releases += 1
        signed = any(
            asset.name.endswith(suffix) for asset in assets for suffix in [".sig", ".minisig"]
        )
        
        if signed:
            total_signed += 1

    if total_releases == 0:
        return inconclusive_result
    
    actual = total_signed / total_releases
    confidence = int(actual * 10)
    
    if actual >= 0.75:
        return TestResult(pass_=True, confidence=confidence)
    
    return TestResult(pass_=False, confidence=10 - confidence)

