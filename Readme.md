# Script for cleaning and monitoring backups for a period

## Сommand line argument mode.
Cleans up old backups older than a specified number of days.
Monitors the relevance of backups based on the presence of files no older than a specified number of days.
```
positional arguments:
  path               Cleared dir

optional arguments:
  -h, --help         show this help message and exit
  -a AGE, --age AGE  Depth save days
  -d, --delete       enable clearing mode
  -m, --monitor      enable monitoring mode
  -v, --verbose      print more information about file

```

## Config file mode
not implemented
