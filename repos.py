import asyncio
import re
import time

from github_requests import get_full_paginated_resource
from utils import format_s


async def get_repo_names_by_org(org: str):
  start = time.process_time_ns()
  print(f'Fetching list of all \'{org}\' repos...')
  base_url = f'https://api.github.com/orgs/{org}/repos'

  pages = await get_full_paginated_resource(base_url)

  repos = []
  for result in pages:
    for repo in result['body']:
      repos.append(repo)

  output = sorted(list(map(lambda x: x['name'], repos)))
  elapsed = time.process_time_ns() - start
  print(f'Got {len(output)} repos ({len(pages)} requests) in {format_s(elapsed)}')

  return output
