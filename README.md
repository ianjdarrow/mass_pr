A simple tool for coordinating mass PRs across an entire GitHub organization.

## Usage

1. `pipenv shell && pipenv install` or `pip3 install -r requirements.txt`.
2. Generate a GitHub API token. (Not strictly necessary, but rate limits will get you for all but the smallest orgs.)
3. Create a `.env` file in the project root. Define `GITHUB_USER` and `GITHUB_TOKEN`.
4. _TBD -- currently, just run `main.py` and get all the users in the IPFS org!_

Tested with Python 3.7.2. Almost definitely requires >= 3.6.
