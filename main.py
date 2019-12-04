"""Greeter.

Usage:
  exporter.py export <env> [--partial] [--config=<filepath>]
  exporter.py import <env> [--partial] [--config=<filepath>]
  exporter.py update <env> [--partial] [--config=<filepath>]
  exporter.py schema <env> [--config=<filepath>]
  exporter.py (-h | --help)

Options:
  -h --help             Show this screen.
  export                Export the remote db and save to csv
  import                Import to local db from csv
  update                Export and import in a single command
  schema                Downlaod the schema (without data)
  --env                 Set the environment (aqua,bright,catalog).
  --partial             Choose if partial import/export (non mandatory)
  --config=<filepath>   Config file path.

"""


import sys
from docopt import docopt
from colorama import init


def main():
    args = docopt(__doc__)

    # if args['--config']:
    #     pass
    # else:
    #     print("Config path not provided!")
    #     sys.exit()
    print("Operation started")



if __name__ == '__main__':
    init()
    main()