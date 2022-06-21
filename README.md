# :moneybag: Payday Event Generator :moneybag:

![example](example.gif)

Payday sometimes is too complicated too remember. For example, the payday occurs on x days before the last day of each month, and cannot be on the weekend. 

This python script helps you simplify your life by just generating the payday events in .ics file format, which can be easily imported to outlook calendar. Currently, it supports 2 payday conditions:
1. Fix date
2. Days before the last day

Both conditions provides the option to avoid the payday on weekend.

## Getting Started 

### Prerequisite

1. Install `VS Code` and `Remote - Containers` extension.
2. `cmd` + `p` and select command `Reopen in Container` ([ref](https://code.visualstudio.com/docs/remote/containers))

### How to run locally

Simply run this command, and answer the interactive questions.
```
python main.py
```

### How to run in docker

Simply run this command, and answer the interactive questions.
```
docker run --rm -it -v ${PWD}/output:/workspace/output bentocast/payday-event-generator:latest
```
