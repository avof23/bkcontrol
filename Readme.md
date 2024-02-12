# Script for cleaning and monitoring backups for a period

## Сommand line argument mode.
Cleans up old backups older than a specified number of days.
Monitors the relevance of backups based on the presence of files no older than a specified number of days.
```
usage: main.py [-h] [-a AGE] [-am AGEMON] [-d] [-m] [-v] [-c CONFIG]
               [path [path ...]]

Clear from old backups and monitoring

positional arguments:
  path                  Cleared dir

optional arguments:
  -h, --help            show this help message and exit
  -a AGE, --age AGE     Clear days
  -am AGEMON, --agemon AGEMON
                        Monitoring days
  -d, --delete          enable clearing mode
  -m, --monitor         enable monitoring mode
  -v, --verbose         print more information about file
  -c CONFIG, --config CONFIG
                        get configuration from file

```

## Config file mode
```
[options]
path=/tmp/examplebkp:/tmp/testbkp
age=90
agemon=7
delete=1
monitor=1
verbose=
email=my@domain.com
```
