"""
Script for cleaning and monitoring backup files for a period specified in days
Work in two modes: command prompt mode and configuration file mode
"""

import os
from datetime import timedelta, datetime
import argparse
import configparser
import smtplib

parser = argparse.ArgumentParser(description="Clear from old backups and monitoring")
parser.add_argument("path", help="Cleared dir", nargs="*")  # position argument
parser.add_argument("-a", "--age", type=int, help='Clear days', default=90)  # option that takes a value
parser.add_argument("-am", "--agemon", type=int, help='Monitoring days', default=7)
parser.add_argument('-d', '--delete', help='enable clearing mode', action='store_true')
parser.add_argument('-m', '--monitor', help='enable monitoring mode', action='store_true')
parser.add_argument('-v', '--verbose', help='print more information about file', action='store_true')  # on/off flag
parser.add_argument('-c', '--config', type=str, help='get configuration from file')  # option that takes a value

args = parser.parse_args()
config = configparser.ConfigParser()
now = datetime.now()

if args.config and os.path.exists(args.config):
    config.read(args.config)
    work_path = config["options"]["path"].split(sep=":")
    args_age = int(config["options"]["age"])
    args_agemon = int(config["options"]["agemon"])
    args_delete = int(config["options"]["delete"])
    args_monitor = int(config["options"]["monitor"])
    args_verbose = int(config["options"]["verbose"])
    alert_type = config["options"]["alert_type"]
    email_receiver = config["mail"]["email"]
    smtp_server = config["mail"]["smtp"]
    port = int(config["mail"]["port"])
    email_sender = config["mail"]["sender"]
else:
    work_path = args.path
    args_age = args.age
    args_agemon = args.agemon
    args_delete = args.delete
    args_monitor = args.monitor
    args_verbose = args.verbose
    alert_type = "console"


def send_alert(dirs_name: list):
    """
    The function generate notification and send via email or console
    :param dirs_name: Directory names for notification in list
    :return: None
    """
    alertmsg = ""
    for dirp in dirs_name:
        alertmsg = (f'{alertmsg}Actual Backups in {dirp} not found!\n'
        f'Backup oldest them: {args_agemon} days.\n')
    alertmsg = f'{alertmsg}Please check your backup job!'

    if alert_type == "email":
        message = (f"Subject: Backup checker Alert\n"
                   f"{alertmsg}")
        with smtplib.SMTP(smtp_server, port) as server:
            server.sendmail(email_sender, email_receiver, message)
    else:
        print(alertmsg)


def clearmonitor(clrpath: str,
                 clrday: int,
                 monday: int,
                 remove: bool = False,
                 mon: bool = True,
                 verb: bool = False
                 ) -> tuple:
    """
    Function find file in specified dir
    :param clrpath: folder to search for files
    :param clrday: files are older than a specified number of days
    :param monday: files are newer than a specified number of days
    :param remove: remove file enable
    :param mon: monitoring enable
    :param verb: verbose output
    :return: tuple include number files to remove and number actual files
    """
    filesclear, filesmon = 0, 0
    if not os.path.exists(clrpath):
        return filesclear, filesmon
    with os.scandir(path=clrpath) as fileobject:
        for file in fileobject:
            statusinfo = os.stat(file)
            if remove and statusinfo.st_mtime < int((now - timedelta(days=clrday)).timestamp()):
                filesclear += 1
                os.remove(file)
                if verb:
                    print(f'{file.name} created: {datetime.fromtimestamp(statusinfo.st_mtime)} - removed!')
            if mon and statusinfo.st_mtime >= int((now - timedelta(days=monday)).timestamp()):
                filesmon += 1
                if verb:
                    print(f'Found actual backup {file.name} created: {datetime.fromtimestamp(statusinfo.st_mtime)}')
    return filesclear, filesmon

path_without_backups = list()

for path in work_path:
    result = clearmonitor(path, args_age, args_agemon, args_delete, args_monitor, args_verbose)
    if alert_type == "console":
        print(f"Processed dir: {path}")
        print(f"Removed {result[0]} files.")

    if args_monitor and not result[1]:
        path_without_backups.append(path)
        # print("Alarm actual backup not found!")
        send_alert(path_without_backups)
