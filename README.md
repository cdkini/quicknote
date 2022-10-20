# quicknote (qn)
quicknote is a terminal-based notetaking system design around speed and ease-of-use.


### Installation
```bash
pip install git+https://github.com/cdkini/quicknote.git
brew install fzf
```

### Setup
```bash
# First, point your root env var at your notes directory
export QN_ROOT=<YOUR_NOTES_PATH>
```
```bash
# Second, configure any relevant settings you might want
qn config
```

These are my settings (which requires additional dependencies of `nvim`, `rg`, and `bat`)
```json
{
    "editor": "nvim",
    "grep_cmd": "rg",
    "git_remote_name": "origin",
    "fzf_opts": "-m --preview \"bat --style=numbers --color=always --line-range :500 {}\""
}
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
