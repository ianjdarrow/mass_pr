import asyncio
from dotenv import load_dotenv, find_dotenv
import github_requests

if __name__ == "__main__":
  load_dotenv(find_dotenv())
  loop = asyncio.get_event_loop()

  repo_future = asyncio.ensure_future(
      github_requests.get_repo_names_by_org('ipfs'))
  repos = loop.run_until_complete(repo_future)
  for repo in repos:
    print(repo)
