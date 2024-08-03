# defold-utils

This is meant to be some kind of shared utilities for myself as I tinker with the [Defold](https://github.com/defold/defold) game engine. Right now I've been using [Zed](https://github.com/zed-industries/zed) as my main text editor, but that might not be the case at some point, so I want to avoid as much as possible being "locked" in a specific text editor.
The goal of the things I build here are to be the most independent of other tools as possible.

This was inspired by [defold-zed](https://github.com/astrochili/defold-zed) and current script implementation was made thanks to the examples on [Defold Kit](https://github.com/astrochili/vscode-defold/)'s repo. The decision to implement in Python was due the fact that my main computers are a macOS machine and a laptop with Fedora, and by my setup Python will probably be always present, as opposed to Node.JS, for instance.

## Compatibility

So far I've made this to work on macOS, tested on a M1 MBP.

## Scripts

### Launch

As a proof of concept I made this small python script which is able to open Defold on at a specific project.

#### Example (Zed)

In Zed one may define a `tasks.json` file, and possibly configure a new task to use this script as:

```json
[
  {
    "label": "launch",
    "command": "python scripts/launch.py",
    "use_new_terminal": false,
    "allow_concurrent_runs": false,
    "reveal": "always"
  }
]
```

It's also possible to assign key bindings to tasks, such as:

```json
[
  {
    "context": "Workspace",
    "bindings": {
      "cmd-d": ["task::Spawn", { "task_name": "launch" }]
    }
  }
]
```

Which will run the *launch* task defined before.
