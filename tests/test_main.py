from typing import Callable, List
from tester.tester import Tester

class TestResult:
    def __init__(self, pass_: bool = False, message: str = "", confidence: int = 0, should_retry: bool = False, error: Exception = None):
        self.pass_ = pass_
        self.message = message
        self.confidence = confidence
        self.should_retry = should_retry
        self.error = error

inconclusive_result = TestResult(pass_=False, confidence=0)
retry_result = TestResult(pass_=False, should_retry=True)

def retry_result_func(error: Exception) -> TestResult:
    r = TestResult(pass_=retry_result.pass_, should_retry=retry_result.should_retry)
    r.error = error
    return r

CheckFn = Callable[[Tester], TestResult]

def multi_check(*fns: CheckFn) -> CheckFn:
    threshold = 7
    
    def wrapper(c: Tester) -> TestResult:
        max_result = TestResult()
        
        for fn in fns:
            result = fn(c)
            if result.confidence > threshold:
                return result
            if result.confidence >= max_result.confidence:
                max_result = result
        
        return max_result
    
    return wrapper

class NamedTest:
    def __init__(self, name: str, fn: CheckFn):
        self.name = name
        self.fn = fn

# create a list with all testes
all_tests: List[NamedTest] = []
