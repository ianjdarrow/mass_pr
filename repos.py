import asyncio
import re
import time

from github_requests import fetch, post, get_full_paginated_resource
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


def remove_existing_licenses(tree: list) -> list:
  return list(filter(lambda x: 'license' not in x['path'].lower(), tree))


def add_file(tree: list, hash: str, path: str) -> list:
  tree.append({
      'path': path,
      'mode': '100644',
      'type': 'blob',
      'sha': hash,
  })
  return tree


async def get_last_commit(org: str, repo: str):
  last_commit = await fetch(f'https://api.github.com/repos/{org}/{repo}/commits')
  parent_hash = last_commit['body'][0]['sha']
  return parent_hash


async def get_master_tree(org: str, repo: str, parent_hash: str):
  last_commit = await fetch(f'https://api.github.com/repos/{org}/{repo}/git/trees/{parent_hash}')
  return last_commit['body']['tree']


async def create_tree(org: str, repo: str, tree: list, parent_hash: str):
  payload = {
      'tree': tree,
      'base_tree': parent_hash
  }
  result = await post(f'https://api.github.com/repos/{org}/{repo}/git/trees', payload)
  print(result)


async def create_blob_from_file(org: str, repo: str, filename: str) -> str:
  file = open(filename).read()
  payload = {
      'content': file,
      'encoding': 'utf-8'
  }
  result = await post(f'https://api.github.com/repos/{org}/{repo}/git/blobs', payload)
  return result['body']['sha']


async def create_commit(org: str, repo: str, parent_hash: str, tree_hash: str, msg: str):
  payload = {
      'parents': [parent_hash],
      'tree': tree_hash,
      'message': msg
  }
  print(payload)
  result = await post(f'https://api.github.com/repos/{org}/{repo}/git/commits', payload)
  return result
