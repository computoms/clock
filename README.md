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
