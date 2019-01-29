import time


def format_s(delta):
  return '{:.3f}s'.format(delta/1e9)


def chunk(data, n):
  for i in range(0, len(data), n):
    yield data[i:i+n]
