from unittest import mock

import pytest

from qn.repo import Repo


def test_add_note_existing_name_raises_error(tmp_path):
    root = tmp_path
    editor = mock.MagicMock()

    repo = Repo(root=root, editor=editor)

    file_name = "foo.md"
    existing_file = root.joinpath(file_name)
    existing_file.touch()

    with pytest.raises(ValueError) as e:
        repo.add_note(file_name)

    assert f"Note '{file_name}' already exists; please use 'qn open'" == str(e.value)


def test_add_note_invokes_editor(tmp_path):
    root = tmp_path
    editor = mock.MagicMock()

    repo = Repo(root=root, editor=editor)

    repo.add_note("foo.md")

    editor.open.assert_called()


def test_open_note_nonexistent_name_raises_error(tmp_path):
    root = tmp_path
    editor = mock.MagicMock()

    repo = Repo(root=root, editor=editor)

    with pytest.raises(ValueError) as e:
        file_names = ("foo.md",)
        repo.open_notes(file_names)

    assert f"Note '{file_names[0]}' does not exist; please use 'qn add'" == str(e.value)


def test_open_note_invokes_editor(tmp_path):
    root = tmp_path
    editor = mock.MagicMock()

    repo = Repo(root=root, editor=editor)

    file_names = ("foo.md", "bar.md")
    for file_name in file_names:
        existing_file = root.joinpath(file_name)
        existing_file.touch()

    repo.open_notes(file_names)

    editor.open.assert_called()
