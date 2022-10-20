# quicknote (qn)
quicknote is a terminal-based notetaking system design around speed and ease-of-use.


### Installation
```bash
pip install git+https://github.com/cdkini/quicknote.git
brew install fzf
```

### Setup
```bash
# Point your root env var at your notes directory
export QN_ROOT=... # Alternatively, add to .bashrc/.zshrc
```

### Commands
```
  add     Create a new note.
  daily   Open your daily note (formatted YYYY-MM-DD).
  grep    Use ripgrep to search through notes.
  ls      List notes.
  open    Open an existing note.
  put     Open a note if it exists else create a new one.
  rm      Delete notes.
  status  Get status of notes with git.
  sync    Sync notes with GitHub.
  web     Open notes in GitHub.
```
