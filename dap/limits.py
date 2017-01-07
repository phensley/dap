
import time


class TokenBucket(object):

    # simple token bucket rate limiter

    def __init__(self, rate):
        self.rate = rate
        self.tokens = 0
        self.prev = time.time()

    def consume(self, tokens):
        if self.rate == 0:
            return 0

        # compute elapsed time
        now = time.time()
        delta = now - self.prev
        self.prev = now

        # calculate tokens added during interval
        self.tokens += delta * self.rate
        if self.tokens > self.rate:
            self.tokens = self.rate

        # compute the sleep time, if any, to maintain target rate
        self.tokens -= tokens
        if self.tokens >= 0:
            return 0
        else:
            return -self.tokens / self.rate

