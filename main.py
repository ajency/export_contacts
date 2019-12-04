"""Greeter.

Usage:
  main.py <env> [--auto]
  main.py (-h | --help)

Options:
  -h --help             Show this screen.
  <env>                Set the environment (aqua,bright,catalog).
  --auto             Choose if partial import/export (non mandatory)

"""


import sys
from docopt import docopt
from colorama import init
from exporter import Exporter
from pathlib import Path
from dotenv import load_dotenv



def main():
    args = docopt(__doc__)
    print(args)

    if args['<env>']:
        pass
    else:
        print("environment not provided!")
        sys.exit()
    exporter = Exporter(args['<env>'], args['--auto'])
    exporter.start()



if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    init()
    main()