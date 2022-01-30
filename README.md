# clock

Simple command-line time tracker.

# Usage

## Tracking tasks

Use the `./clock` command to start working on a new task:

```
$ ./clock Definition of the prototype +myapp +proto
```

You can add tags / projects so your tasks (`+tag`) or identifiers (`.id`).

To switch to a new tas, just use the same command:

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

Several filters are available. Default is to show all the tasks, ordered by first tag.

To show all the tasks with their details:

```
$ ./clock show --details
```

To filter by a tag:

```
$ ./clock show +tag
```

