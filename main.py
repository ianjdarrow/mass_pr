import asyncio
from dotenv import load_dotenv, find_dotenv

import github_requests
import contributors
import repos


if __name__ == "__main__":
  load_dotenv(find_dotenv())
  loop = asyncio.get_event_loop()
  repos = loop.run_until_complete(
      repos.get_repo_names_by_org('ipfs'))
  contributors = loop.run_until_complete(
      contributors.get_lots_of_contributors('ipfs', repos))
  print(sorted(contributors))
  print(f'Got {len(contributors)} contributors!')
