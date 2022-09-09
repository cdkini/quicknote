### quicknote (qn)


### Requirements
* fzf
* bat
* rg
* nvim


### Commands
```bash
Usage: qn [OPTIONS] COMMAND [ARGS]...

  qn (quicknote) is a terminal-based notetaking system designed around speed
  and ease-of-use.

Options:
  --help  Show this message and exit.

Commands:
  add     Create a new note.
  grep    Use ripgrep through parse through notes.
  ls      List notes.
  open    Open an existing note.
  put     Open a note if it exists else create a new one.
  rm      Delete notes.
  status  Get status of notes with git.
  sync    Sync notes using git.
```


### Useful Aliases
```
# Create a daily note
qn put $(date +%Y-%m-%d)

# Open the last accessed note
qn open "$(qn ls -s accessed -r | head -n 1)"
```
