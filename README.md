# MIMI AI

MIMI is a lightweight futuristic AI command center for Termux, powered by `tgpt`.

## Features

- AI chat, coding assistance, and web-search prompts
- Safe file analysis with bounded input
- Optional Termux text-to-speech
- Autonomous insight mode, stopped with `Ctrl+C`
- Local memory and JSON settings under `~/.mimi`
- Rich terminal dashboard and plugin status view

## Requirements

- Android with Termux from F-Droid or GitHub
- Network access
- Node.js/npm and Python 3
- Optional: the Termux:API app for voice output

## Install

Run the installer inside Termux:

```sh
curl -fsSL https://raw.githubusercontent.com/Karlfiner-Robotiken/mimi/main/mimi-installer.sh | bash
```

The installer is idempotent, creates the `mimi` launcher in `$PREFIX/bin`, validates the downloaded Python source, and starts MIMI when complete. Set `MIMI_NO_LAUNCH=1` if you only want to install it.

For testing a different source revision:

```sh
MIMI_SOURCE_URL=https://raw.githubusercontent.com/Karlfiner-Robotiken/mimi/<revision>/mimi.py \
  MIMI_NO_LAUNCH=1 bash mimi-installer.sh
```

## Usage

```sh
mimi
```

MIMI stores settings in `~/.mimi/settings.json` and conversation labels in `~/.mimi/memory/history.txt`. Use Settings to toggle memory, animation, or voice behavior. Never paste secrets into prompts or commit your local memory files.

## Troubleshooting

- `tgpt` missing: run `npm install -g tgpt` and confirm `node --version` works.
- Voice unavailable: install the Termux:API app and run `pkg install termux-api`.
- Broken settings: delete `~/.mimi/settings.json`; MIMI recreates it with defaults.
- Permission errors: keep the project inside Termux's home directory and rerun the installer.

## Development and release

Validate changes before publishing:

```sh
python -m py_compile mimi.py
bash -n mimi-installer.sh
MIMI_NO_LAUNCH=1 bash mimi-installer.sh
```

Changes should be developed on a feature branch and merged through a pull request. After merging, the installer serves the `main` branch source and can be published through the GitHub repository's normal release path.
