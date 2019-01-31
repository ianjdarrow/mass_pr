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
#   repos = loop.run_until_complete(
#       repos.get_repo_names_by_org(args['org']))
#   contributors = loop.run_until_complete(
#       contributors.get_lots_of_contributors(args['org'], repos))
#   for name, contributions in sorted(contributors.items(), key=lambda t: t[1], reverse=True):
#     print(f'[ ] @{name} ({contributions})')
#   print(f'Got {len(contributors)} contributors!')

  parent_hash = loop.run_until_complete(
      repos.get_last_commit("mass-pr-test-org", "project-1"))
#   tree = loop.run_until_complete(repos.get_master_tree(
#       "mass-pr-test-org", "project-1", parent_hash))
#   stripped = repos.remove_existing_licenses(tree)
#   mit_blob_hash = loop.run_until_complete(repos.create_blob_from_file(
#       "mass-pr-test-org", "project-1", "./assets/LICENSE-MIT"))
#   restored = repos.add_file(stripped, mit_blob_hash, 'LICENSE-MIT')
#   result = loop.run_until_complete(repos.create_tree(
#       "mass-pr-test-org", "project-1", restored, parent_hash))

  tree_hash = '121b262971fe2b96421d0a6be707728461906269'
  new_commit = loop.run_until_complete(repos.create_commit(
      "mass-pr-test-org", "project-1", parent_hash, tree_hash, "Update to MIT license"))
  print(new_commit)
