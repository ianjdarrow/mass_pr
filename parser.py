import argparse


def parse():
  parser = argparse.ArgumentParser(description='Get GitHub stuff.')
  parser.add_argument('org', metavar='<org_name>', type=str,
                      help='the name of the org to pull all repos and contributors')
  args = parser.parse_args()
  return {
      'org': args.org
  }
