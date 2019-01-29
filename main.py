import asyncio
from dotenv import load_dotenv, find_dotenv

import github_requests
import contributors
import parser
import repos


if __name__ == "__main__":
  load_dotenv(find_dotenv())
  args = parser.parse()
  loop = asyncio.get_event_loop()
  repos = loop.run_until_complete(
      repos.get_repo_names_by_org(args['org']))
  contributors = loop.run_until_complete(
      contributors.get_lots_of_contributors(args['org'], repos))
  print(sorted(contributors))
  print(f'Got {len(contributors)} contributors!')
