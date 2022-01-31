# clock

Simple command-line time tracker based on a simple text file format.

# Introduction

This simple utility uses a text file to store tasks with date/time information. Each time you start working on a task, a new line is created on the file with the current time and a description of the task you are starting to work on.

At the end of the day, or anytime, you can then generate reports and statistics based on the file.

## File structure

The file structure is very simple, as shown below:

```
[2022-01-01]
10:00 Starting project X +projectX
11:23 Starting documentation of project X +projectX +doc
12:00 [Stop]
[2022-01-02]
08:05 Starting workday, checking emails +office +emails
09:00 Back on documentation +projectX +doc
10:00 [Stop]
```

## Tags and ids

An entry in this file can be associated with tags if you start the tag with a `+` (`+tag`) or ID if you start with a `.` (`.456`). 

Tags allow for powerful filtering and reporting. They are ordered, meaning that `+project +doc` is different from `+doc +project` (see reports and filters below).

IDs allow to track time of tasks from an external tool, such as Jira. Entries with an ID are automatically assigned a default tag (`+jira`).

# Script usage

## Tracking tasks

Use the `./clock` command to start working on a new task:

```
$ ./clock Definition of the prototype +myapp +proto
Added: 08:10 Definition of the prototype +myapp +proto

Duration   Date                  Start      Stop       Tags            Name                               IDs
00:00      2022-01-01            08:10      08:10      +myapp,+proto   Definition of the prototype         
```

To switch to a new task, just use the same command:

```
$ ./clock Switching to new task
Added: 09:02 Switching to a new task

Duration   Date                  Start      Stop       Tags            Name                               IDs
00:00      2022-01-01            08:10      08:10                      Switching to a new task
```

This will automatically stop the last task and start a new one. When you have finished working, use the `stop` command:

```
$ ./clock stop
Added: 10:00 [Stop]
```

## Reports

You can show reports/statistics with the `show` command:

```
$ ./clock show
```

All tasks are ordered by first tag by default. Several filters are available, see `./clock --help` for the full documentation.

To show all the tasks with their details:

```
$ ./clock show --details
```

To filter by a tag:

```
$ ./clock show +tag
```

To filter by an ID:

```
$ ./clock show .345
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