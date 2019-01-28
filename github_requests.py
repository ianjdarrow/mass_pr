from base64 import b64encode
from collections.abc import MutableMapping
import asyncio
import re
import requests
import os


def get_authenticated_client() -> requests.Session:
  c = requests.Session()
  c.headers.update({'Authorization': get_auth_header(),
                    'Accept': 'application/vnd.github.inertia-preview+json',
                    'User-Agent': 'ianjdarrow'})
  return c


async def get_repo_names_by_org(org: str):
  c = get_authenticated_client()
  base_url = f'https://api.github.com/orgs/{org}/repos'

  repos = []

  resp = c.get(base_url)
  headers = resp.headers
  print(f'Rate limit remaining: {headers["X-RateLimit-Remaining"]}/5000')

  for repo in resp.json():
    repos.append(repo)

  page_count = get_page_count_from_headers(headers)

  tasks = []
  for page in range(1, page_count+1):
    url = f'{base_url}?page={page}'
    task = asyncio.ensure_future(fetch(c, url))
    tasks.append(task)

  results = await asyncio.gather(*tasks)
  for result in results:
    for repo in result.json():
      repos.append(repo)

  return sorted(list(map(lambda x: x['name'], repos)))


async def fetch(client, url):
  print(f'GET {url}')
  resp = client.get(url)
  return resp


def get_page_count_from_headers(header: MutableMapping) -> int:
  if not 'Link' in header:
    return 1
  [_, last_link] = header['Link'].split(', ')
  m = re.search(r'page=(\d+)', last_link)
  if m:
    return int(m.group(1))
  raise Exception("Error traversing pagination")


def get_auth_header() -> str:
  # todo: replace with dotenv
  username = os.getenv('GITHUB_USER')
  token = os.getenv("GITHUB_TOKEN")
  encoded = b64encode(f'{username}:{token}'.encode('utf-8')).decode('utf-8')
  return f'Basic {encoded}'
