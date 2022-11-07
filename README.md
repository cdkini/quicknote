# quicknote (qn)
*quicknote is a terminal-based notetaking system designed around speed and ease-of-use.*

The primary philosophy when designing this tool was to make recording quick thoughts or ideas as simple as possible without hampering productivity.
For the terminal power user and UNIX enthusiast, having the ability to take notes in the same environment without context-switching is incredibly useful.

The efficiency of this program comes with a cost - the overall feature set is quite limited.
If you take meticulous, interconnected notes through a more robust PKM system, please use [Obsidian](https://obsidian.md/) or another tool better suited for your needs.

### Setup
```bash
# Install quicknote and any required external dependencies
pip install git+https://github.com/cdkini/quicknote.git
brew install fzf ripgrep bat

# Point your root env var at your desired notes directory
export QN_ROOT=$HOME/notes # Or other existing directory

# Configure your editor
export EDITOR="nvim" # Or other valid terminal-based editor
```

### Commands
```
Primary Commands:
  add     Create a new note.
  upsert  Update a note if it exists or create a new one.
  open    Open note(s).
  grep    Search through notes.
  ls      List notes.
  rm      Delete note(s).

Misc Commands:
  status  Get status of notes with Git.
  sync    Sync notes with GitHub.
  web     Open notes in GitHub.
```
