import os
import sys
from datetime import timedelta, datetime
import argparse
import configparser

parser = argparse.ArgumentParser(description="Clear from old backups")
parser.add_argument("path", help="Cleared dir") # position argument
parser.add_argument("-a", "--age", type=int, help='Depth save days', default=90) # option that takes a value
parser.add_argument('-d', '--delete', help='enable clearing mode', action='store_true')
parser.add_argument('-m', '--monitor', help='enable monitoring mode', action='store_true')
parser.add_argument('-v', '--verbose', help='print more information about file', action='store_true')  # on/off flag

args = parser.parse_args()
now = datetime.now()

#config = configparser.ConfigParser()
#config.read("config.ini")

#print(config["Twitter"]["username"])


def monitoring(monpath: str, alarmday: int) -> str:
    pass


def clearmonitor(clrpath: str, depthday: int) -> int:
    filesfound = 0
    with os.scandir(path=clrpath) as fileobject:
        for file in fileobject:
            statusinfo = os.stat(file)
            if args.delete and statusinfo.st_mtime < int((now - timedelta(days=depthday)).timestamp()):
                filesfound += 1
                os.remove(file)
                if args.verbose:
                    print(f'{file.name} created: {datetime.fromtimestamp(statusinfo.st_mtime)} - removed!')
            if args.monitor and statusinfo.st_mtime >= int((now - timedelta(days=depthday)).timestamp()):
                filesfound += 1
                if args.verbose:
                    print(f'Found actual backup {file.name} created: {datetime.fromtimestamp(statusinfo.st_mtime)}')
    return filesfound


print(f"Processed dir: {args.path}")
if args.age:
    print(f"Find files oldest: {args.age} days")

result = clearmonitor(args.path, args.age)
if args.monitor and not result:
    print("Alarm actual backup not found!")
if args.delete:
    print(f"Removed {result} files.")
