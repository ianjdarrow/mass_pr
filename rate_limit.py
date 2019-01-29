import asyncio
import time


class RateLimiter:
  RATE = 5  # requests/second
  MAX_TOKENS = 10

  def __init__(self, client):
    self.client = client
    self.tokens = self.MAX_TOKENS
    self.updated_at = time.monotonic()

  async def get(self, *args, **kwargs):
    await self.wait_for_token()
    return self.client.get(*args, **kwargs)

  async def wait_for_token(self):
    while self.tokens <= 1:
      self.add_new_tokens()
      await asyncio.sleep(0.5)
    self.tokens -= 1

  def add_new_tokens(self):
    now = time.monotonic()
    time_since_update = now - self.updated_at
    new_tokens = time_since_update * self.RATE
    if self.tokens + new_tokens >= 1:
      self.tokens = min(self.tokens, self.MAX_TOKENS)
      self.updated_at = now
