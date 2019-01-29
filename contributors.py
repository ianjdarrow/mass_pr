import asyncio
import re
import time
from functools import reduce
from yaspin import yaspin

from github_requests import get_full_paginated_resource
from utils import chunk, format_s


def format_contributor_url(org: str, repo: str) -> str:
  return f'https://api.github.com/repos/{org}/{repo}/contributors'


async def get_contributors_by_org_repo(org: str, repo: str):
  # start = time.process_time_ns()
  # print(f'Fetching list of all \'{org}/{repo}\' contributors...')
  base_url = format_contributor_url(org, repo)

  pages = await get_full_paginated_resource(base_url)

  contributors = []
  for result in pages:
    for contributor in result['body']:
      contributors.append(contributor)

  output = list(map(lambda x: x['login'], contributors))
  # elapsed = time.process_time_ns() - start
  # print(f'Got {org}/{repo}, ({len(output)} requests) in {format_s(elapsed)}')
  return output


async def get_lots_of_contributors(org: str, repos: [str]):
  results = set([])
  with yaspin(text=f"Fetching all {org} contributors..") as spinner:
    tasks = [get_contributors_by_org_repo(org, repo) for repo in repos]
    pieces = chunk(tasks, 20)
    for piece in pieces:
      contributors = await asyncio.gather(*piece)
      for repo in contributors:
        results.update(repo)
      await asyncio.sleep(1)
    spinner.ok('✅ ')

  return results
