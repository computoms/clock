# clock

Simple command-line time tracker.

# Usage

## Tracking tasks

Use the `./clock` command to start working on a new task:

```
$ ./clock Definition of the prototype +myapp +proto
```

You can add tags / projects to your tasks (`+tag`) or identifiers (`.id`).

To switch to a new task, just use the same command:

```
$ ./clock Switching to new task
```

This will automatically stop the last task and start a new one. When you have finished working, use the `stop` command:

```
$ ./clock stop
```

## Reports

You can show the times with the `show` command:

```
$ ./clock show
```

Several filters are available. See `./clock --help` for the full documentation.

Default is to show all the tasks, ordered by first tag.

To show all the tasks with their details:

```
$ ./clock show --details
```

To filter by a tag:

```
$ ./clock show +tag
```

## Examples

Show today's tasks:

![Show today's tasks](https://github.com/computoms/clock/blob/main/img/today.png?raw=true)

Show tasks by tags:

![Show tasks by +myapp tag](https://github.com/computoms/clock/blob/main/img/myapp.png?raw=true)

Show today's tasks details:

![Show today's tasks details](https://github.com/computoms/clock/blob/main/img/details.png?raw=true)

## Documentation

```
usage: clock [-h] [-a HH:MM] [-c] [-f FILE] [-t] [-w] [-s YYYY-mm-dd]
             [-e YYYY-mm-dd] [-T HH:MM] [-D HH:MM] [-d]
             command

Helps managing time tracking

positional arguments:
  command

optional arguments:
  -h, --help            show this help message and exit
  -a HH:MM, --at HH:MM  <add> Specify a time (format HH:MM) of a new entry
  -c, --current         <add> Modify the description of the current entry
  -f FILE, --file FILE  Speficy the file to store time entries. Default is
                        ./clock.txt
  -t, --today           <show> Show only entries from today
  -w, --week            <show> Show only entries from the current week
  -s YYYY-mm-dd, --from YYYY-mm-dd
                        <show> Include entries with start date later or equal
                        to given date (format YYYY-mm-dd)
  -e YYYY-mm-dd, --to YYYY-mm-dd
                        <show> Include entries with start date earlier or
                        equal to given date (format YYYY-mm-dd)
  -T HH:MM, --target HH:MM
                        <show> Sets expected target time (format HH:MM) and
                        computes the difference with actual times in the
                        reports
  -D HH:MM, --target-per-day HH:MM
                        <show> Sets expected target time per day (format
                        HH:MM) and computes the difference with actual times
                        in the reports
  -d, --details         <show> Shows detailed report
```