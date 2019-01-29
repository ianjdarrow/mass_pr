from base64 import b64encode
import aiohttp
import asyncio
import os
import re


def get_authenticated_client() -> aiohttp.ClientSession:
  headers = {'Authorization': create_auth_header(
  ), 'Accept': 'application/vnd.github.inertia-preview+json', 'User-Agent': os.getenv("GITHUB_USER")}
  return aiohttp.ClientSession(headers=headers)


async def fetch(url: str):
  async with get_authenticated_client() as c:
    async with c.get(url) as response:
      body = None
      try:
        body = await response.json()
      except:
        print(response)
        body = ''
      return {
          "headers": response.headers,
          "status": response.status,
          "body": body
      }


async def get_full_paginated_resource(base_url: str):
  response = await fetch(base_url)

  headers = response['headers']
  remaining = headers["X-RateLimit-Remaining"]
  limit = headers["X-RateLimit-Limit"]
  print(f'Rate limit remaining: {remaining}/{limit}')
  page_count = get_page_count_from_headers(headers)

  results = [response]

  if page_count == 1:
    return results

  page_range = range(2, page_count+1)
  tasks = [fetch(f'{base_url}?page={page}') for page in page_range]

  all_responses = await asyncio.gather(*tasks)
  results += all_responses

  return results


def create_auth_header() -> str:
  username = os.getenv('GITHUB_USER')
  token = os.getenv("GITHUB_TOKEN")
  encoded = b64encode(f'{username}:{token}'.encode('utf-8')).decode('utf-8')
  return f'Basic {encoded}'


def get_page_count_from_headers(header) -> int:
  if not 'Link' in header:
    return 1
  [_, last_link] = header['Link'].split(', ')
  m = re.search(r'page=(\d+)', last_link)
  if m:
    return int(m.group(1))
  raise Exception("Error traversing pagination")
