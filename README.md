# quicknote (qn)
quicknote is a terminal-based notetaking system design around speed and ease-of-use.


### Installation
```bash
pip install git+https://github.com/cdkini/quicknote.git
brew install fzf
```

### Setup
```bash
# 1. Point your root env var at your notes directory
export QN_ROOT=<YOUR_NOTES_PATH>

# 2. Configure any relevant settings
qn config
```

### Commands
```
Primary Commands:
  add     Create a new note.
  open    Open note(s).
  grep    Search through notes.
  ls      List notes.
  rm      Delete note(s).

Misc Commands:
  config  Configure settings.
  status  Get status of notes with Git.
  sync    Sync notes with GitHub.
  web     Open notes in GitHub.
```
