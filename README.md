# quicknote (qn)
*quicknote is a terminal-based notetaking system designed around speed and ease-of-use.*

The primary philosophy when designing this tool was to make recording quick thoughts or ideas as simple as possible without hampering productivity.
For the terminal power user and UNIX enthusiast, having the ability to take notes in the same environment without context-switching is incredibly useful.

The efficiency of this program comes with a cost - the overall feature set is quite limited.
If you take meticulous, interconnected notes through a more robust PKM system, please use [Obsidian](https://obsidian.md/) or another tool better suited for your needs.

### Setup
```bash
# 1. Install quicknote and any required CLI tools
pip install git+https://github.com/cdkini/quicknote.git
brew install fzf

# 2. Point your root env var at your desired notes directory
export QN_ROOT=$HOME/notes # Or other existing directory

# 3. Configure any relevant settings you might want
qn config
```

### Configuration
I use the following settings (which require additional external dependencies of `nvim`, `rg`, and `bat`):
```json
{
   "editor": "nvim",
   "grep_cmd": "rg",
   "git_remote_name": "origin",
   "fzf_opts": "-m --preview \"bat --style=numbers --color=always --line-range :500 {}\""
}
```
Additionally, I use [vimwiki](https://github.com/vimwiki/vimwiki) to leverage the library's referencing and tagging capabilities.

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
